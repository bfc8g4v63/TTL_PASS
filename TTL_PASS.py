#$ TTL_PASS.py 
#% 設定 TTL=65 並自動關閉 Apple 熱點 IPv6 (v15)

import ctypes
import sys
import subprocess
import os
import json

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    script = os.path.abspath(sys.argv[0])
    pyexe = sys.executable
    params = subprocess.list2cmdline([pyexe, script, "--elevated"])
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", f'/k {params}', None, 1
        )
        sys.exit(0)
    except Exception:
        sys.exit(1)

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                encoding="utf-8",
                                errors="ignore")
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception:
        return 1, "", "指令執行失敗"

def set_ttl(value: int):
    cmd = f'netsh int ipv4 set glob defaultcurhoplimit={value}'
    return run_cmd(cmd)

def check_ttl():
    code, out, err = run_cmd("ping -n 1 127.0.0.1")
    if code != 0:
        return "無法讀取 TTL"
    for line in out.splitlines():
        if "TTL=" in line.upper():
            return line.strip()
    return "無法讀取 TTL"

def find_apple_adapter_desc():
    cmd = 'Get-NetAdapter | Select-Object -Property Name, InterfaceDescription | ConvertTo-Json'
    code, out, err = run_cmd(f'powershell -Command "{cmd}"')
    if code != 0 or not out:
        return None, None
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            data = [data]
        for item in data:
            desc = item.get("InterfaceDescription", "")
            if "Apple Mobile Device Ethernet" in desc:
                return item.get("Name"), desc
    except Exception:
        return None, None
    return None, None

def ipv6_status_by_desc(description):
    cmd = f"Get-NetAdapterBinding | Where-Object {{$_.InterfaceDescription -eq '{description}' -and $_.ComponentID -eq 'ms_tcpip6'}} | ConvertTo-Json"
    code, out, err = run_cmd(f"powershell -Command \"{cmd}\"")
    if code != 0 or not out:
        return None
    try:
        data = json.loads(out)
        return data.get("Enabled", None)
    except Exception:
        return None

def disable_ipv6_by_desc(description):
    status = ipv6_status_by_desc(description)
    if status is False:
        return 0, "IPv6 已經是關閉狀態", ""
    cmd = f"Get-NetAdapterBinding | Where-Object {{$_.InterfaceDescription -eq '{description}' -and $_.ComponentID -eq 'ms_tcpip6'}} | Disable-NetAdapterBinding -PassThru"
    return run_cmd(f"powershell -Command \"{cmd}\"")

def wait_at_end():
    try:
        input("\n按 Enter 結束")
    except Exception:
        try:
            os.system("pause")
        except Exception:
            pass

def main():
    if not is_admin():
        if "--elevated" not in sys.argv:
            relaunch_as_admin()
        else:
            wait_at_end()
            return

    print("正在將 TTL 設定為 65 ...")
    code, out, err = set_ttl(65)
    if code != 0:
        print("設定失敗:", err or out)
    else:
        print("TTL 設定完成")

    ttl_info = check_ttl()
    print("Ping 127.0.0.1 回應:", ttl_info)

    if "TTL=" in ttl_info and "65" in ttl_info:
        print("TTL 設定成功。")
    else:
        print("TTL 可能未正確套用。")

    print("\n正在偵測 Apple 熱點網卡 ...")
    name, desc = find_apple_adapter_desc()
    if not desc:
        print("找不到 Apple Mobile Device Ethernet")
    else:
        print(f"找到網卡: {name} ({desc})，正在檢查 IPv6 狀態 ...")
        code, out, err = disable_ipv6_by_desc(desc)
        if code != 0:
            print("IPv6 關閉失敗:", err or out)
        else:
            print(out or "IPv6 已成功關閉。")

    wait_at_end()

if __name__ == "__main__":
    main()
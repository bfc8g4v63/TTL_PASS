#$ TTL自動修正工具 (TTL_PASS.py)
#% 功能：自動進行系統網路優化（支援 USB 熱點與 Wi-Fi 熱點，修正所有亂碼）

import ctypes
import sys
import subprocess
import os
import json
import locale

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

def run_cmd(cmd, use_locale=False):
    enc = locale.getpreferredencoding(False) if use_locale else "utf-8"
    try:
        result = subprocess.run(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                encoding=enc,
                                errors="ignore")
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception:
        return 1, "", "指令執行失敗"

def run_ps(ps_cmd):
    full = f'powershell -NoProfile -Command "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; {ps_cmd}"'
    return run_cmd(full)

def set_ttl(value: int):
    return run_cmd(f'netsh int ipv4 set glob defaultcurhoplimit={value}', use_locale=True)

def check_ttl():
    code, out, err = run_cmd("ping -n 1 127.0.0.1", use_locale=True)
    if code != 0:
        return "無法檢測"
    for line in out.splitlines():
        if "TTL=" in line.upper():
            return line.strip()
    return "無法檢測"

def find_apple_adapter_desc():
    code, out, err = run_ps('Get-NetAdapter | Select-Object Name,InterfaceDescription | ConvertTo-Json')
    if code != 0 or not out:
        return None, None
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            data = [data]
        for item in data:
            if "Apple Mobile Device Ethernet" in item.get("InterfaceDescription",""):
                return item.get("Name"), item.get("InterfaceDescription")
    except Exception:
        return None, None
    return None, None

def find_wifi_adapter_connected():
    code, out, err = run_cmd('netsh wlan show interfaces', use_locale=True)
    if code != 0 or not out:
        return None, None
    name, ssid = None, None
    for line in out.splitlines():
        line=line.strip()
        if line.lower().startswith("name"):
            parts=line.split(":",1)
            if len(parts)==2: name=parts[1].strip().strip('"')
        elif line.lower().startswith("ssid"):
            parts=line.split(":",1)
            if len(parts)==2: ssid=parts[1].strip().strip('"')
        if name and ssid: break
    if not name:
        return None, None
    code, out, err = run_ps(f"Get-NetAdapter | Where-Object {{$_.Name -eq '{name}'}} | Select-Object Name,InterfaceDescription | ConvertTo-Json")
    if code != 0 or not out:
        return name, None
    try:
        data=json.loads(out)
        if isinstance(data,dict): desc=data.get("InterfaceDescription","")
        elif isinstance(data,list) and data: desc=data[0].get("InterfaceDescription","")
        else: desc=None
        return name, desc
    except Exception:
        return name, None

def ipv6_status_by_desc(description):
    ps = f"Get-NetAdapterBinding | Where-Object {{$_.InterfaceDescription -eq '{description}' -and $_.ComponentID -eq 'ms_tcpip6'}} | ConvertTo-Json"
    code, out, err = run_ps(ps)
    if code != 0 or not out:
        return None
    try:
        data=json.loads(out)
        return data.get("Enabled",None)
    except Exception:
        return None

def disable_ipv6_by_desc(description):
    status=ipv6_status_by_desc(description)
    if status is False:
        return 0,"介面已完成優化",""
    ps=f"Get-NetAdapterBinding | Where-Object {{$_.InterfaceDescription -eq '{description}' -and $_.ComponentID -eq 'ms_tcpip6'}} | Disable-NetAdapterBinding -PassThru"
    return run_ps(ps)

def wait_at_end():
    try:
        input("\n按 Enter 結束")
    except Exception:
        pass

def main():
    if not is_admin():
        if "--elevated" not in sys.argv:
            relaunch_as_admin()
        else:
            wait_at_end()
            return

    print("正在進行系統網路優化 ...")
    code, out, err = set_ttl(65)
    print("網路參數已更新" if code==0 else "設定時發生錯誤")

    ttl_info = check_ttl()
    print("狀態檢查:", ttl_info)

    print("\n正在偵測連線介面 ...")
    name, desc = find_apple_adapter_desc()
    if not desc:
        name, desc = find_wifi_adapter_connected()
    if not desc:
        print("未偵測到可用連線介面")
    else:
        print(f"已偵測到介面: {name}")
        code, out, err = disable_ipv6_by_desc(desc)
        print("連線介面已完成優化設定" if code==0 else "優化設定未完全套用")

    wait_at_end()

if __name__ == "__main__":
    main()
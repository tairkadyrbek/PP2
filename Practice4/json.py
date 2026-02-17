import json

with open("sample-data.json", "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f'{"":35} {"Description":20} {"Speed":8} {"MTU":6}')
print(f'{"-"*35} {"-"*20} {"-"*8} {"-"*6}')

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    
    dn = attrs["dn"]
    
    short_dn = dn.replace("topology/pod-1",  "")
    
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]
    
    print(f"{short_dn:35} {descr:20} {speed:8} {mtu:6}")
    

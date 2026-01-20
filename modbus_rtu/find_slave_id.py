from pymodbus.client import ModbusTcpClient

IP = "172.16.22.87"
PORT = 502

client = ModbusTcpClient(IP, port=PORT)
client.connect()

found_units = []

for unit_id in range(1, 248):
    try:
        result = client.read_holding_registers(
            address=0,
            count=1,
           
        )

        if not result.isError():
            print(f"✅ Tìm thấy Slave ID: {unit_id}")
            found_units.append(unit_id)

    except Exception:
        pass

client.close()

print("Danh sách Slave ID tìm được:", found_units)

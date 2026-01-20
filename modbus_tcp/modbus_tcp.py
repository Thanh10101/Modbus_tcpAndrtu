from pymodbus.client import ModbusTcpClient

IP = "172.16.22.87"
PORT = 502


client = ModbusTcpClient(IP, port=PORT)
client.connect()

valid_addresses = []

for addr in range(0, 200):  # quét 0 → 199
    result = client.read_holding_registers(
        address=addr,
        count=1,
    
    )

    if not result.isError():
        print(f"✅ Address {addr} có giá trị: {result.registers[0]}")
        valid_addresses.append(addr)

client.close()

print("Address hợp lệ:", valid_addresses)

from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("172.16.22.87", port=502)

if client.connect():
    print("Kết nối Modbus TCP thành công")

    response = client.read_holding_registers(
    address=0,
    count=2
    )


    if not response.isError():
        print("Giá trị:", response.registers)
    else:
        print("Lỗi đọc Modbus")

    client.close()
else:
    print("Không kết nối được PLC")

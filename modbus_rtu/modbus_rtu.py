from pymodbus.client import ModbusSerialClient
import time

PORT = "COM1"           # đổi cho đúng
TEST_ADDRESS = 0        # 40001
ADDRESS_RANGE = 50      # quét 0 → 49

baudrates = [1200, 2400, 4800, 9600, 19200]
parities = ["N", "E", "O"]

results = {}

print("\n🔍 BƯỚC 1: DÒ BAUDRATE + PARITY")

for baud in baudrates:
    for parity in parities:
        client = ModbusSerialClient(
            port=PORT,
            baudrate=baud,
            parity=parity,
            stopbits=1,
            bytesize=8,
            timeout=1
        )

        if not client.connect():
            continue

        try:
            test = client.read_holding_registers(
                address=TEST_ADDRESS,
                count=1,
                slave=1
            )

            if test.isError():
                client.close()
                continue

            print(f"✅ OK baud={baud}, parity={parity}")

            print("  🔍 BƯỚC 2: DÒ SLAVE ID")
            for slave in range(1, 248):
                try:
                    resp = client.read_holding_registers(
                        address=TEST_ADDRESS,
                        count=1,
                        slave=slave
                    )

                    if resp.isError():
                        continue

                    print(f"    ✅ Slave ID={slave}")

                    print("    🔍 BƯỚC 3: DÒ ADDRESS")
                    for addr in range(0, ADDRESS_RANGE):
                        try:
                            r = client.read_holding_registers(
                                address=addr,
                                count=1,
                                slave=slave
                            )

                            if not r.isError():
                                key = (baud, parity, slave, addr)
                                results[key] = r.registers[0]

                        except Exception:
                            pass

                except Exception:
                    pass

        except Exception:
            pass

        client.close()
        time.sleep(0.3)

print("\n🎉 KẾT QUẢ CUỐI CÙNG:\n")

for k, v in results.items():
    baud, parity, slave, addr = k
    print(
        f"baud={baud:6} | parity={parity} | slave={slave:3} | "
        f"address={addr:3} | value={v}"
    )

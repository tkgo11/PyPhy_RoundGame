# PhyPi_RoundGame
# 설명

이 코드는 MicroPython을 사용하여 NeoPixel과 SSD1306 OLED 디스플레이, Bluetooth 저에너지(BLE)를 사용하여 동작하는 게임을 구현합니다. 이 게임은 사용자가 게임을 시작하고 포인트를 얻는 간단한 로직을 포함하고 있습니다.

## 구성 요소

- **MicroPython**: 이 코드가 실행되는 플랫폼으로, 주로 마이크로 컨트롤러에서 사용됩니다.
- **SSD1306 디스플레이**: 게임 상태를 화면에 출력합니다.
- **NeoPixel**: 다양한 색상의 LED 표시를 위해 사용됩니다.
- **Bluetooth**: BLE를 통해 게임을 시작하고 이벤트를 수신합니다.

## 코드 설명

### 초기화

```python
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

pin = Pin(14, Pin.OUT)
np = NeoPixel(pin, 12)

ble = bluetooth.BLE()
p = ble_library.BLESimplePeripheral(ble, "Game")
```

    I2C를 통해 디스플레이와 NeoPixel을 초기화합니다.
    BLE를 초기화하여 "Game"이라는 이름으로 주변 기기를 설정합니다.

게임 로직
```
# 초기화
for i in range(0, 12):
    np[i] = (0, 0, 0)
np.write()

# 변수 지정
isClockWise = bool(randint(0, 1))
isGameStarted = False
isPoint = False

speed = 0.25
rad = 3
pos_list = list()
score = 0

display.fill(0)
display.text('Ready', 48, 28, 1)
display.show()
```

    NeoPixel을 끄고 초기화합니다.
    게임 상태 및 변수들을 설정합니다.

Bluetooth 이벤트 처리
```
def on_rx(v):
    # 이벤트를 수신하고 게임 시작 또는 종료 처리
```
    Bluetooth로부터 수신된 명령에 따라 게임을 시작하거나 점수를 처리합니다.

게임 루프
```
while True:
    if isGameStarted:
        # 게임 진행 상황을 처리
    else:
        # 대기 상태 표시
```
    게임이 시작되면 점수를 계산하고 LED를 업데이트합니다.
    게임이 시작되지 않으면 대기 상태를 표시합니다.

코드 사용법

    MicroPython가 지원되는 마이크로컨트롤러에 코드를 업로드합니다.
    게임을 시작하려면 Bluetooth 장치에서 "START_GAME" 명령을 송신합니다.
    NeoPixel이 명령에 따라 반응하며 점수를 업데이트 합니다.

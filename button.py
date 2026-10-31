import time
import RPi.GPIO as GPIO

# Khai báo danh sách các chân GPIO (theo chuẩn BCM)
pins = [4, 27, 17, 22]

GPIO.setmode(GPIO.BCM)

for pin in pins:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
  print(f"Đang lắng nghe tín hiệu 3.3V trên GPIO {pins}... Nhấn Ctrl+C để thoát.")

  while True:
    for pin in pins:
      if GPIO.input(pin) == GPIO.HIGH:
        print(f"--> Phát hiện tín hiệu 3.3V tại GPIO {pin}")

    time.sleep(0.1)

except KeyboardInterrupt:
  print("\nĐang dọn dẹp và thoát chương trình...")
  GPIO.cleanup()

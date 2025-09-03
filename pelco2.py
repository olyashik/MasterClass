import time
import subprocess

def set_rotator_position(azimuth, elevation):
    try:
        # Формируем команду rotctl
        cmd = ["rotctl", "-m", "2", "-r", "0.0.0.0:4533", "P", f"{azimuth}", f"{elevation}"]
        
        # Выполняем команду
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            print(f"{azimuth}", f"{elevation}")
        else:
            print(f"Ошибка: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e.stderr}")
    except FileNotFoundError:
        print("Ошибка: rotctl не найден. Убедитесь, что он установлен и добавлен в PATH.")

def set_rotator_zero (azimut_poz, elevation_poz):
    if azimut_poz > 0: 
        set_rotator_position(-10,0)
        time.sleep(abs((azimut_poz) * 0.141111))
    elif azimut_poz < 0: 
        set_rotator_position(10,0)
        time.sleep(abs((azimut_poz) * 0.141111))
    set_rotator_position(0,0)

    if elevation_poz > 45: 
        set_rotator_position(0,10)
        time.sleep(abs((elevation_poz-45) * 0.210185*4))
    elif elevation_poz < 45: 
        set_rotator_position(0,90)
        time.sleep(abs((elevation_poz - 45) * 0.210185*4))
    set_rotator_position(0,0)

azimut_poz = 0
elevation_poz = 45
time_azimut = 0
time_elevation = 0
print("Количество повторений цикла: ")
flag = int(input())

while flag!=0:

    print("Азимут и элевация': ")
    azimuth_in, elevation_in = map(float, input().split())

    # Перевод из градусов во время с учётом текущего положения
    time_azimut = abs((azimuth_in - azimut_poz) * 0.141111)
    time_elevation = abs((elevation_in - elevation_poz) * 0.210185*4)

    if time_azimut == time_elevation:
        set_rotator_position (azimuth_in, elevation_in)
        time.sleep(time_azimut)
    elif time_azimut == 0: 
        set_rotator_position (0, elevation_in)
        time.sleep(time_elevation)
    elif time_elevation == 0: 
        set_rotator_position (azimuth_in, 0)
        time.sleep(time_azimut)
    elif time_azimut > time_elevation:
        set_rotator_position (azimuth_in, elevation_in)
        time.sleep(time_elevation)
        set_rotator_position (azimuth_in, 0)
        time.sleep(time_azimut - time_elevation)
    elif time_elevation > time_azimut:
        set_rotator_position (azimuth_in, elevation_in)
        time.sleep(time_azimut)
        set_rotator_position (0, elevation_in)
        time.sleep(time_elevation - time_azimut)
    set_rotator_position (0, 0)
    azimut_poz = azimuth_in
    elevation_poz = elevation_in
    flag -= 1

print("Ожидание магии...")
time.sleep(5)
set_rotator_zero (azimut_poz, elevation_poz)








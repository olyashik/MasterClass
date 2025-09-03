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


# Возвращение устройства в исходное положение 
def set_rotator_zero(azimuth_timenz, elevation_timenz):

    # Возвращение верхнего мотора
    set_rotator_position(-azimuth_timenz, 0)
    time.sleep(abs(azimuth_timenz))
    set_rotator_position(0, 0)

    # Возвращение нижнего мотора
    if elevation_timenz > 0:
        set_rotator_position(0, 10)
        time.sleep(abs(elevation_timenz))
    elif elevation_timenz < 0:
        set_rotator_position(0, 90)
        time.sleep(abs(elevation_timenz))
    set_rotator_position(0, 0)



# Исходные данные
time0_azimuth = 0
time0_elevation = 0

print("Есть контакт!")
print("Какое количество выполнений цикла хотите, босс? ")
flag = int(input())

# Цикл для поворота устройства по времени определённое количество раз
while flag != 0:
    
    print("Введите направление вращения и время поворота: ")
    azimuth_in, elevation_in, time_azimuth_in, time_elevation_in = map(float, input().split())

    if azimuth_in > 0: time0_azimuth += time_azimuth_in
    elif azimuth_in < 0: time0_azimuth -= time_azimuth_in 
    else: time0_azimuth -= 0

    if elevation_in > 44: time0_elevation += time_elevation_in
    elif 0 < elevation_in < 44: time0_elevation -= time_elevation_in
    else: time0_elevation += 0

    if time_azimuth_in == time_elevation_in:
        set_rotator_position(azimuth_in, elevation_in)
        time.sleep(time_azimuth_in)
    elif time_elevation_in == 0:
        set_rotator_position(azimuth_in, 0)
        time.sleep(time_azimuth_in)
    elif time_azimuth_in == 0:
        set_rotator_position(0, elevation_in)
        time.sleep(time_elevation_in)
    elif time_azimuth_in > time_elevation_in:
        set_rotator_position(azimuth_in, elevation_in)
        time.sleep(time_elevation_in)
        set_rotator_position(azimuth_in, 0)
        time.sleep(time_azimuth_in - time_elevation_in)
    else:
        set_rotator_position(azimuth_in, elevation_in)
        time.sleep(time_azimuth_in)
        set_rotator_position(0, elevation_in)
        time.sleep(time_elevation_in - time_azimuth_in) 
    set_rotator_position(0, 0)
    time.sleep(0.1)
    flag -= 1

print("Магия начнётся черз 5 секундочек!!!")
time.sleep(5)
set_rotator_zero(time0_azimuth, time0_elevation)
time0_elevation = 0
time0_azimuth = 0
print("Спасибо за внимание!")
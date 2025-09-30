"""

Se eliminó el basic.forever que detenía la melodía al dejar de agitar

"""
# Servo en posición 0°
def checkPassword():
    global unlocked, entered
    if entered == password:
        unlocked = True
        # Encender LED verde (P15) y pin 2
        pins.digital_write_pin(DigitalPin.P15, 1)
        pins.digital_write_pin(DigitalPin.P2, 1)
        # Sonido de contraseña correcta
        music.start_melody(music.built_in_melody(Melodies.ENTERTAINER),
            MelodyOptions.ONCE)
        # Mostrar ✓
        basic.show_icon(IconNames.YES)
        # Mover servo a 90°
        pins.servo_write_pin(AnalogPin.P2, 90)
        # Esperar 3 segundos antes de apagar pines y mover servo a 0°
        basic.pause(3000)
        # Apagar LED verde y pin 2
        pins.digital_write_pin(DigitalPin.P15, 0)
        pins.digital_write_pin(DigitalPin.P2, 0)
        # Volver servo a 0°
        pins.servo_write_pin(AnalogPin.P2, 0)
        # Borrar pantalla
        basic.clear_screen()
    else:
        unlocked = False
        # Encender LED rojo (P13)
        pins.digital_write_pin(DigitalPin.P13, 1)
        # Sonido de contraseña incorrecta
        music.start_melody(music.built_in_melody(Melodies.WAWAWAWAA),
            MelodyOptions.ONCE)
        # Mostrar ✗
        basic.show_icon(IconNames.NO)
        # Esperar 5 segundos
        basic.pause(5000)
        # Apagar LED rojo y limpiar pantalla
        pins.digital_write_pin(DigitalPin.P13, 0)
        basic.clear_screen()
    # Reiniciar intento
    entered = ""
# Mostrar temperatura al presionar logo

def on_logo_pressed():
    global temp
    if unlocked:
        temp = input.temperature()
        basic.show_number(temp)
        if temp > 20:
            # Temperatura menor a 100°C
            # Encender LED en pin 1
            pins.digital_write_pin(DigitalPin.P1, 1)
            # Reproducir melodía de temperatura baja
            music.start_melody(music.built_in_melody(Melodies.FUNK), MelodyOptions.ONCE)
            # Esperar 5 segundos
            basic.pause(5000)
            # Apagar LED en pin 1 y detener melodía
            pins.digital_write_pin(DigitalPin.P1, 0)
            music.stop_melody(MelodyStopOptions.ALL)
        basic.clear_screen()
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)

# Ingreso de contraseña con botones A y B

def on_button_pressed_a():
    global entered
    if not (unlocked):
        entered = "" + entered + "A"
input.on_button_pressed(Button.A, on_button_pressed_a)

# Detectar agitación para alarma con duración de 4 segundos

def on_gesture_shake():
    if unlocked:
        basic.show_icon(IconNames.SKULL)
        # Solo una vez
        music.start_melody(music.built_in_melody(Melodies.POWER_DOWN),
            MelodyOptions.ONCE)
        # Esperar 4 segundos
        basic.pause(4000)
        music.stop_melody(MelodyStopOptions.ALL)
        basic.clear_screen()
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# Validar contraseña con botón A+B

def on_button_pressed_ab():
    if not (unlocked):
        checkPassword()
input.on_button_pressed(Button.AB, on_button_pressed_ab)

def on_button_pressed_b():
    global entered
    if not (unlocked):
        entered = "" + entered + "B"
input.on_button_pressed(Button.B, on_button_pressed_b)

temp = 0
unlocked = False
entered = ""
password = ""
password = "ABA"
# Apagar todos los pines al inicio
# LED rojo apagado
pins.digital_write_pin(DigitalPin.P13, 0)
# LED verde apagado
pins.digital_write_pin(DigitalPin.P15, 0)
# LEDs blancos apagados
pins.digital_write_pin(DigitalPin.P16, 0)
# LED azul apagado
pins.digital_write_pin(DigitalPin.P1, 0)
# Servo en posición 0°
pins.servo_write_pin(AnalogPin.P2, 0)
# Sensor de luz controla LEDs blancos en pin 16

def on_forever():
    if unlocked:
        if input.light_level() < 150:
            # Enciende LEDs blancos
            pins.digital_write_pin(DigitalPin.P16, 1)
        else:
            # Apaga LEDs blancos
            pins.digital_write_pin(DigitalPin.P16, 0)
    else:
        # Asegura que estén apagados si está bloqueado
        pins.digital_write_pin(DigitalPin.P16, 0)
basic.forever(on_forever)

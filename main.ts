/**
 * Se eliminó el basic.forever que detenía la melodía al dejar de agitar
 */
// Servo en posición 0°
function checkPassword () {
    if (entered == password) {
        unlocked = true
        // Encender LED verde (P15) y pin 2
        pins.digitalWritePin(DigitalPin.P15, 1)
        pins.digitalWritePin(DigitalPin.P2, 1)
        // Sonido de contraseña correcta
        music.startMelody(music.builtInMelody(Melodies.Entertainer), MelodyOptions.Once)
        // Mostrar ✓
        basic.showIcon(IconNames.Yes)
        // Mover servo a 90°
        pins.servoWritePin(AnalogPin.P2, 90)
        // Esperar 3 segundos antes de apagar pines y mover servo a 0°
        basic.pause(3000)
        // Apagar LED verde y pin 2
        pins.digitalWritePin(DigitalPin.P15, 0)
        pins.digitalWritePin(DigitalPin.P2, 0)
        // Volver servo a 0°
        pins.servoWritePin(AnalogPin.P2, 0)
        // Borrar pantalla
        basic.clearScreen()
    } else {
        unlocked = false
        // Encender LED rojo (P13)
        pins.digitalWritePin(DigitalPin.P13, 1)
        // Sonido de contraseña incorrecta
        music.startMelody(music.builtInMelody(Melodies.Wawawawaa), MelodyOptions.Once)
        // Mostrar ✗
        basic.showIcon(IconNames.No)
        // Esperar 5 segundos
        basic.pause(5000)
        // Apagar LED rojo y limpiar pantalla
        pins.digitalWritePin(DigitalPin.P13, 0)
        basic.clearScreen()
    }
    // Reiniciar intento
    entered = ""
}
// Ingreso de contraseña con botones A y B
input.onButtonPressed(Button.A, function () {
    if (!(unlocked)) {
        entered = "" + entered + "A"
    }
})
// Validar contraseña con botón A+B
input.onButtonPressed(Button.AB, function () {
    if (!(unlocked)) {
        checkPassword()
    }
})
input.onButtonPressed(Button.B, function () {
    if (!(unlocked)) {
        entered = "" + entered + "B"
    }
})
// Detectar agitación para alarma con duración de 4 segundos
input.onGesture(Gesture.Shake, function () {
    if (unlocked) {
        basic.showIcon(IconNames.Skull)
        // Solo una vez
        music.startMelody(music.builtInMelody(Melodies.PowerDown), MelodyOptions.Once)
        // Esperar 4 segundos
        basic.pause(4000)
        music.stopMelody(MelodyStopOptions.All)
        basic.clearScreen()
    }
})
// Mostrar temperatura al presionar logo
input.onLogoEvent(TouchButtonEvent.Pressed, function () {
    if (unlocked) {
        temp = input.temperature()
        basic.showNumber(temp)
        if (temp > 20) {
            // Temperatura menor a 100°C
            // Encender LED en pin 1
            pins.digitalWritePin(DigitalPin.P1, 1)
            // Reproducir melodía de temperatura baja
            music.startMelody(music.builtInMelody(Melodies.Funk), MelodyOptions.Once)
            // Esperar 5 segundos
            basic.pause(5000)
            // Apagar LED en pin 1 y detener melodía
            pins.digitalWritePin(DigitalPin.P1, 0)
            music.stopMelody(MelodyStopOptions.All)
        }
        basic.clearScreen()
    }
})
let temp = 0
let unlocked = false
let entered = ""
let password = ""
password = "ABA"
// Apagar todos los pines al inicio
// LED rojo apagado
pins.digitalWritePin(DigitalPin.P13, 0)
// LED verde apagado
pins.digitalWritePin(DigitalPin.P15, 0)
// LEDs blancos apagados
pins.digitalWritePin(DigitalPin.P16, 0)
// LED azul apagado
pins.digitalWritePin(DigitalPin.P1, 0)
// Servo en posición 0°
pins.servoWritePin(AnalogPin.P2, 0)
// Sensor de luz controla LEDs blancos en pin 16
basic.forever(function () {
    if (unlocked) {
        if (input.lightLevel() < 150) {
            // Enciende LEDs blancos
            pins.digitalWritePin(DigitalPin.P16, 1)
        } else {
            // Apaga LEDs blancos
            pins.digitalWritePin(DigitalPin.P16, 0)
        }
    } else {
        // Asegura que estén apagados si está bloqueado
        pins.digitalWritePin(DigitalPin.P16, 0)
    }
})

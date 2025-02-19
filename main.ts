OLED12864_I2C.init(60)
OLED12864_I2C.zoom(false)
OLED12864_I2C.clear()
// OLED12864_I2C.show_number(0, 0, 12, 1)
pins.digitalWritePin(DigitalPin.P3, 0)
let toggle = 0
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    if (toggle == 0) {
        pins.digitalWritePin(DigitalPin.P1, 1)
        pins.digitalWritePin(DigitalPin.P2, 0)
        pins.digitalWritePin(DigitalPin.P3, 0)
        toggle = 1
    } else if (toggle == 1) {
        pins.digitalWritePin(DigitalPin.P1, 0)
        pins.digitalWritePin(DigitalPin.P2, 1)
        pins.digitalWritePin(DigitalPin.P3, 0)
        toggle = 2
    } else if (toggle == 2) {
        pins.digitalWritePin(DigitalPin.P1, 0)
        pins.digitalWritePin(DigitalPin.P2, 0)
        pins.digitalWritePin(DigitalPin.P3, 1)
        toggle = 0
    }
    
    console.log(toggle)
})
// OLED12864_I2C.show_string(0, 0, "A 7 6 20 8", 1)
// OLED12864_I2C.show_string(0, 3, "K A 9 20 8", 1)
function win_round() {
    music.play(music.tonePlayable(Note.C, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    win_round()
})

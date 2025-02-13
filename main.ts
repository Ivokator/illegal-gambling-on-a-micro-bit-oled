OLED12864_I2C.init(60)
OLED12864_I2C.zoom(false)
OLED12864_I2C.clear()
function king_card(position: number = 0) {
    let i: number;
    OLED12864_I2C.rect(position * 20, 0, position * 20 + 16, 22, 1)
    //  Making the 'K'
    OLED12864_I2C.vline(position * 20 + 3, 4, 13, 3)
    //  Diagonal lines
    for (i = 0; i < 7; i++) {
        OLED12864_I2C.pixel(position * 20 + 4 + i, 10 - i, 1)
    }
    for (i = 0; i < 7; i++) {
        OLED12864_I2C.pixel(position * 20 + 4 + i, 10 + i, 1)
    }
}

function queen_card(position: number = 0) {
    let i: number;
    OLED12864_I2C.rect(position * 20, 0, position * 20 + 16, 22, 1)
    //  Making the 'Q'
    OLED12864_I2C.vline(position * 20 + 3, 4, 13, 3)
    for (i = 0; i < 7; i++) {
        OLED12864_I2C.pixel(position * 20 + 4 + i, 10 - i, 1)
    }
    for (i = 0; i < 7; i++) {
        OLED12864_I2C.pixel(position * 20 + 4 + i, 10 + i, 1)
    }
}

OLED12864_I2C.showNumber(0, 0, 12, 1)
pins.digitalWritePin(DigitalPin.P3, 0)
let toggle = 0
function on_button_pressed_b() {
    
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
}

//  input.on_button_pressed(Button.B, on_button_pressed_b)
// OLED12864_I2C.show_string(0, 0, "A 7 6 20 8", 1)
// OLED12864_I2C.show_string(0, 3, "K A 9 20 8", 1)
function win_round() {
    music.play(music.tonePlayable(Note.C, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    win_round()
})

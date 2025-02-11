OLED12864_I2C.init(60)
function king_card(position: number = 0) {
    OLED12864_I2C.rect(position * 10, 0, position * 10 + 8, 11, 1)
    OLED12864_I2C.vline(2, 3, 5, 1)
    OLED12864_I2C.pixel(3, 5, 1)
    OLED12864_I2C.pixel(4, 4, 1)
    OLED12864_I2C.pixel(4, 6, 1)
    OLED12864_I2C.pixel(5, 3, 1)
    OLED12864_I2C.pixel(5, 7, 1)
}

OLED12864_I2C.zoom(false)
OLED12864_I2C.showString(0, 0, "A 7 6 10 8", 1)
OLED12864_I2C.showString(0, 3, "K A 9 10 8", 1)
function win_round() {
    music.play(music.tonePlayable(Note.C, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    win_round()
})

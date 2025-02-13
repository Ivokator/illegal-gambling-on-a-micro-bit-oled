OLED12864_I2C.init(60)
OLED12864_I2C.zoom(False)
OLED12864_I2C.clear()


def king_card(position = 0):
    OLED12864_I2C.rect((position*20), 0, (position*20) + 16, 22, 1)

    # Making the 'K'
    OLED12864_I2C.vline((position*20) + 3, 4, 13, 3)
    
    # Diagonal lines
    for i in range(7):
        OLED12864_I2C.pixel((position*20) + 4 + i, 10 - i, 1)
    for i in range(7):
            OLED12864_I2C.pixel((position*20) + 4 + i, 10 + i, 1)


def queen_card(position = 0):
    OLED12864_I2C.rect((position*20), 0, (position*20) + 16, 22, 1)

    # Making the 'Q'
    OLED12864_I2C.vline((position*20) + 3, 4, 13, 3)
    
    for i in range(7):
        OLED12864_I2C.pixel((position*20) + 4 + i, 10 - i, 1)
    for i in range(7):
            OLED12864_I2C.pixel((position*20) + 4 + i, 10 + i, 1)


OLED12864_I2C.show_number(0, 0, 12, 1)


pins.digital_write_pin(DigitalPin.P3, 0)


toggle = 0

def on_button_pressed_b():
    global toggle
    if toggle == 0:
        pins.digital_write_pin(DigitalPin.P1, 1)
        pins.digital_write_pin(DigitalPin.P2, 0)
        pins.digital_write_pin(DigitalPin.P3, 0)
        toggle = 1
    elif toggle == 1:
        pins.digital_write_pin(DigitalPin.P1, 0)
        pins.digital_write_pin(DigitalPin.P2, 1)
        pins.digital_write_pin(DigitalPin.P3, 0)
        toggle = 2
    elif toggle == 2:
        pins.digital_write_pin(DigitalPin.P1, 0)
        pins.digital_write_pin(DigitalPin.P2, 0)
        pins.digital_write_pin(DigitalPin.P3, 1)
        toggle = 0
    print(toggle)
# input.on_button_pressed(Button.B, on_button_pressed_b)



#OLED12864_I2C.show_string(0, 0, "A 7 6 20 8", 1)
#OLED12864_I2C.show_string(0, 3, "K A 9 20 8", 1)






def win_round():
    music.play(music.tone_playable(Note.C, music.beat(BeatFraction.WHOLE)), music.PlaybackMode.UNTIL_DONE)

def on_button_pressed_a():
    win_round()
input.on_button_pressed(Button.A, on_button_pressed_a)
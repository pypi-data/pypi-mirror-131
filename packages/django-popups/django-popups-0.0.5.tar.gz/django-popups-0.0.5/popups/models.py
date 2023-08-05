from django.db import models


class Popups(models.Model):
    BLACK = 'BL'
    GRAY = 'GR'
    WHITE = 'WH'

    COLOR_CHOICES = [
        (BLACK, '검정색'),
        (GRAY, '회색'),
        (WHITE, '횐색'),
    ]

    BLUE_PAPER = 'BP'
    RED_XMAS = 'RX'
    YELLOW_PAPER = 'YP'
    RED_LINES = 'RL'
    WHITE_PRESENT = 'WP'

    BACKGROUND_CHOICES = [
        (BLUE_PAPER, '파란 종이 배경'),
        (RED_XMAS, '붉은 크리스마스 배경'),
        (YELLOW_PAPER, '미색 구겨진 종이 배경'),
        (RED_LINES, '진은 붉은색 선 배경'),
        (WHITE_PRESENT, '흰 선물상자 배경'),
    ]

    title = models.CharField('제목', max_length=20)
    subtitle = models.CharField('부제목', max_length=40)
    text_color = models.CharField(max_length=2, choices=COLOR_CHOICES, default=BLACK)
    background = models.CharField(max_length=2, choices=BACKGROUND_CHOICES, default=BLUE_PAPER)
    url = models.URLField('참고링크', blank=True, null=True, help_text="공란 가능")
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.title


class ImagePopups(Popups):
    image = models.ImageField(upload_to=f'images/popups/')


class NotiPopups(Popups):
    ICON_CHOICE = [
        ('CAL', 'Calender'),
        ('BELL', 'Bell-Ring'),
    ]
    icon = models.CharField(max_length=10, choices=ICON_CHOICE, default='BELL')
    description = models.TextField('세부 설명', null=True, blank=True, help_text="줄넘기기 : <br>, 강조 : <strong></strong>")


class EventPopups(Popups):
    preprice = models.CharField('행사전', max_length=20)
    saleprice = models.CharField('행사가', max_length=20)
    target = models.CharField('대상', max_length=20, blank=True, null=True, help_text="공란 가능")
    period = models.CharField('행사기간', max_length=20, blank=True, null=True, help_text="공란 가능")
    description = models.CharField('세부 설명 (예외 사항등)', max_length=50, null=True, blank=True, help_text="공란 가능")

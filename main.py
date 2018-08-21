import random, pygame
import matplotlib.pyplot as plt
from pygame.locals import *
from virus import VirusNode
from doctor import Doctor
pygame.init()

size = (width, height) = (850, 480)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (26, 255, 255)
font = pygame.font.SysFont(None, 70)
bacteria = pygame.sprite.Group()
doctors = pygame.sprite.Group()
doc_num = 1
bac_num = 5
split_time = 500
success = 0
tests = 0
round_over = False
display = False
done = False
case_samples = 10
split_times = 10
test_data = []


def timeout():
    for i in range(300):
        clock.tick(60)
        process_events()


def init():
    global round_over
    bacteria.empty()
    doctors.empty()
    round_over = False
    for i in range(bac_num):
        bacteria.add(VirusNode((random.randint(50, width-50), random.randint(50, height-50)), split_time))
    for i in range(doc_num):
        doctors.add(Doctor((random.randint(50, width-50), random.randint(50, height-50))))


def end_of_round():
    global tests, success, doc_num, bac_num, split_time, done
    if display:
        timeout()
    tests += 1
    if tests >= case_samples:
        test_data.append([doc_num, bac_num, split_time, tests, success / tests * 100])
        print(test_data[-1])
        if test_data[-1][-1] == 0:
            doc_num += 2
        elif test_data[-1][-1] <= 75:
            doc_num += 1
        else:
            split_time = round(split_time*0.9)
            if split_time < 10:
                done = True
        tests = 0
        success = 0
    init()


def process_data():
    x = []
    y = []
    for row in test_data:
        if row[-1] >= 75:
            x.append(row[2])
            y.append(row[0])
    fig = plt.figure()
    plt.scatter(x, y)
    plt.title('Doctors needed to prevent an outbreak\n started by 5 bacteria')
    plt.xlabel('split time (refreshes)')
    plt.ylabel('Doctors Needed')
    fig.savefig('data.png')


def process_events():
    global display, done
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                display = not display


def main():
    global success, round_over
    init()
    while not done:
        if display:
            clock.tick(60)
        process_events()
        if len(bacteria) > bac_num*split_times:
            text = font.render("You were overrun", True, (255, 0, 0))
            text_rect = text.get_rect()
            round_over = True
        elif len(bacteria) == 0:
            text = font.render("Outbreak stopped", True, (255, 0, 0))
            text_rect = text.get_rect()
            success += 1
            round_over = True
        else:
            doctors.update()
            bacteria.update()
            pygame.sprite.groupcollide(doctors, bacteria, False, True)
            text = font.render("Bacteria Count: {}".format(len(bacteria)), True, (255, 0, 0))
            text_rect = text.get_rect()
        if display:
            screen.fill(color)
            doctors.draw(screen)
            bacteria.draw(screen)
            screen.blit(text, text_rect)
            pygame.display.flip()
        if round_over:
            end_of_round()
    process_data()


if __name__ == "__main__":
    main()

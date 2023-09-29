import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, game_settings, screen, player, bullets):
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_UP:
        player.moving_up = True
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, player, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, player):
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
    elif event.key == pygame.K_UP:
        player.moving_up = False
    elif event.key == pygame.K_DOWN:
        player.moving_down = False


def check_events(game_settings, screen, stats, sb, play_button, player, aliens, bullets):
    # Respond to key presses and mouse actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, player, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, sb, play_button, player, aliens, bullets, mouse_x, mouse_y)


def update_screen(game_settings, screen, stats, sb, player, aliens, bullets, play_button):
    # Update images on the screen
    # Redraw the screen
    screen.fill(game_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    player.blitme()
    aliens.draw(screen)

    # Draw the score
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    # Make the screen visible
    pygame.display.flip()


def update_bullets(game_settings, screen, stats, sb, player, aliens, bullets):
    # Removing unnecessary bullets
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings, screen, stats, sb, player, aliens, bullets)


def check_bullet_alien_collisions(game_settings, screen, stats, sb, player, aliens, bullets):

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(game_settings, screen, player, aliens)


def update_aliens(game_settings, stats, screen, sb, player, aliens, bullets):
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(player, aliens):
        ship_hit(game_settings, stats, screen, sb, player, aliens, bullets)

    check_aliens_bottom(game_settings, stats, screen, sb, player, aliens, bullets)


def fire_bullet(game_settings, screen, player, bullets):
    if len(bullets) < game_settings.bullets_max_number:
        new_bullet = Bullet(game_settings, screen, player)
        bullets.add(new_bullet)


def get_number_aliens_x(game_settings, alien_width):
    # Determine how much space is available and how many aliens can fit in it
    available_space_x = game_settings.width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    # Same but with rows
    available_space_y = game_settings.height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in a row
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(game_settings, aliens):

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):

    for alien in aliens.sprites():
        alien.rect.y += game_settings.alien_drop_speed
    game_settings.alien_speed *= -1


def ship_hit(game_settings, stats, screen, sb, player, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, player, aliens)
        player.center_ship()

        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game_settings, stats, screen, sb, player, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, sb, player, aliens, bullets)
            break


def check_play_button(game_settings, screen, stats, sb, play_button, player, aliens, bullets, mouse_x, mouse_y):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settngs
        game_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, player, aliens)
        player.center_ship()


def check_high_score(stats, sb):
    # Check if the score beats high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('record.txt', 'w') as out:
            print(stats.high_score, file=out)
        sb.prep_high_score()




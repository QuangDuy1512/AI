import pygame

def load_tile_images(image_path, size, tile_size):
    """
    Chia ảnh thành các mảnh vuông nhỏ tương ứng với số lượng ô puzzle.

    Args:
        image_path (str): đường dẫn ảnh
        size (int): số hàng/cột của puzzle (3, 4, 5...)
        tile_size (int): kích thước mỗi ô

    Returns:
        (tiles, original_image): list các mảnh ảnh, ảnh gốc đã resize
    """
    image = pygame.image.load(image_path).convert()
    image = pygame.transform.scale(image, (tile_size * size, tile_size * size))

    tiles = []

    for row in range(size):
        for col in range(size):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            tile = image.subsurface(rect).copy()
            tiles.append(tile)

    # Trả về list các mảnh ảnh và bản gốc (dùng để hiển thị mẫu nếu cần)
    return tiles[:-1], image  # Bỏ ô cuối (ô trống = 0)


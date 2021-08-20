from PIL import Image
import sys
import math

INF = math.inf

# Como usar: python3 maze.py image.png

# ------------------------------------------------------------------
# main
def main():

    # Assegurar o uso correto
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 maze.py image.png")

    # Guardar nome do ficheiro
    filename = 'images/' + sys.argv[1]

    # Abrir imagem
    im = Image.open(filename)

    # Guardar a altura e o comprimento da imagem
    width, height = im.size;

    # Converter para RGB
    rgb_im = im.convert('RGB')

    #  Criar matriz (labirinto) e guardar a posição da entrada e de saída
    matrix, entrance_w, exit_w = create_maze(rgb_im, height, width)

    # Resolver o labirinto
    matrix=solve_maze(matrix, entrance_w)

    # Encontrar o caminho do labirinto
    matrix=maze_path(matrix, height, exit_w)

    # Guadar imagem com caminho a vermelho
    draw_path(rgb_im, matrix, height, width, sys.argv[1])


# ------------------------------------------------------------------
# Criar matriz (labirinto)
def create_maze(rgb_im, height, width):

    # Criar uma matriz com o tamanho da imgem
    matrix = [[0 for x in range(height)] for y in range(width)] 

    # Passar a imagem para a matriz (1's == paredes; 0's == caminho)
    for i in range(height):
        for j in range(width):
            r, g, b = rgb_im.getpixel((j, i))
            
            if (r == 0 and g == 0 and b == 0):
                matrix[i][j] = 1
            elif(r == 255 and g == 255 and b == 255):
                matrix[i][j] = 0

    # Assinalar a entrada e a saída (entrada == 2; saída == INF)
    entrance = False
    exit = False

    for k in range(width):
        if(entrance == False and matrix[0][k] == 0):
            matrix[0][k] = 2
            entrance_w = k
            entrance = True
        if(exit == False and matrix[height - 1][width - k - 1] == 0):
            matrix[height - 1][width - k - 1] = INF
            exit_w = width - k - 1
            exit = True

    return matrix, entrance_w, exit_w


# ------------------------------------------------------------------
# Resolver labirinto usando o algoritmo Depth-First Search
def solve_maze(matrix, entrance_w):

    # Fazer o primeiro passo
    matrix[1][entrance_w] = 3

    # Quadrado atual
    pos_h = 1
    pos_w = entrance_w

    # Descobrir caminho
    solved = False

    while(solved == False):
        # Guadar elemento
        pos = matrix[pos_h][pos_w]

        # Verificar se o elemento é a saída
        if(matrix[pos_h][pos_w - 1] == INF or matrix[pos_h][pos_w + 1] == INF
        or matrix[pos_h - 1][pos_w] == INF or matrix[pos_h + 1][pos_w] == INF):
            if(matrix[pos_h][pos_w - 1] == INF):
                matrix[pos_h][pos_w - 1] = pos + 1
            elif(matrix[pos_h][pos_w + 1] == INF):
                matrix[pos_h][pos_w + 1] = pos + 1
            elif(matrix[pos_h - 1][pos_w] == INF):
                matrix[pos_h - 1][pos_w] = pos + 1
            elif(matrix[pos_h + 1][pos_w] == INF):
                matrix[pos_h + 1][pos_w] = pos + 1
            solved = True

        # Caminho sem saída
        elif(matrix[pos_h][pos_w - 1] != 0 and matrix[pos_h][pos_w + 1] != 0
        and matrix[pos_h - 1][pos_w] != 0 and matrix[pos_h + 1][pos_w] != 0):
            # Caminho para a esquerda
            if(matrix[pos_h][pos_w - 1] == pos - 1 and pos - 1 != 1 and pos - 1 != 2):
                pos_w = pos_w - 1
            # Caminho para a direita
            elif(matrix[pos_h][pos_w + 1] == pos - 1 and pos - 1 != 1 and pos - 1 != 2):
                pos_w = pos_w + 1
            # Caminho para cima
            elif(matrix[pos_h - 1][pos_w] == pos - 1 and pos - 1 != 1 and pos - 1 != 2):
                pos_h = pos_h - 1
            # Caminho para baixo
            elif(matrix[pos_h + 1][pos_w] == pos - 1 and pos - 1 != 1 and pos - 1 != 2):
                pos_h = pos_h + 1

        # Avançar um passo
        else:
            # Caminho para a esquerda
            if(matrix[pos_h][pos_w - 1] == 0):
                matrix[pos_h][pos_w - 1] = pos + 1
                pos_w = pos_w - 1
            # Caminho para a direita
            elif(matrix[pos_h][pos_w + 1] == 0):
                matrix[pos_h][pos_w + 1] = pos + 1
                pos_w = pos_w + 1
            # Caminho para cima
            elif(matrix[pos_h - 1][pos_w] == 0):
                matrix[pos_h - 1][pos_w] = pos + 1
                pos_h = pos_h - 1
            # Caminho para baixo
            elif(matrix[pos_h + 1][pos_w] == 0):
                matrix[pos_h + 1][pos_w] = pos + 1
                pos_h = pos_h + 1

    return matrix


# ------------------------------------------------------------------
# Encontrar o caminho
def maze_path(matrix, height, exit_w):

    # Fazer o primeiro passo
    matrix[height - 1][exit_w] = -1

    # Encontrar caminho
    path = False

    # Guardar posição da saída
    pos_h = height - 2
    pos_w = exit_w

    while(path == False):
        # Guadar elemento
        pos = matrix[pos_h][pos_w]

        # Verificar se o elemento é a entrada
        if(matrix[pos_h][pos_w - 1] == 2 or matrix[pos_h][pos_w + 1] == 2
        or matrix[pos_h - 1][pos_w] == 2 or matrix[pos_h + 1][pos_w] == 2):
            if(matrix[pos_h][pos_w - 1] == 2):
                matrix[pos_h][pos_w] = -1
                matrix[pos_h][pos_w - 1] = -1
            elif(matrix[pos_h][pos_w + 1] == 2):
                matrix[pos_h][pos_w] = -1
                matrix[pos_h][pos_w + 1] = -1
            elif(matrix[pos_h - 1][pos_w] == 2):
                matrix[pos_h][pos_w] = -1
                matrix[pos_h - 1][pos_w] = -1
            elif(matrix[pos_h + 1][pos_w] == 2):
                matrix[pos_h][pos_w] = -1
                matrix[pos_h + 1][pos_w] = -1
            path = True

        # Avançar um passo
        else:
            # Caminho para a esquerda
            if(matrix[pos_h][pos_w - 1] == pos - 1):
                matrix[pos_h][pos_w] = -1
                pos_w = pos_w - 1
            # Caminho para a direita
            elif(matrix[pos_h][pos_w + 1] == pos - 1):
                matrix[pos_h][pos_w] = -1
                pos_w = pos_w + 1
            # Caminho para cima
            elif(matrix[pos_h - 1][pos_w] == pos - 1):
                matrix[pos_h][pos_w] = -1
                pos_h = pos_h - 1
            # Caminho para baixo
            elif(matrix[pos_h + 1][pos_w] == pos - 1):
                matrix[pos_h][pos_w] = -1
                pos_h = pos_h + 1
    
    return matrix


# ------------------------------------------------------------------
# Guadar imagem com caminho a vermelho
def draw_path(rgb_im, matrix, height, width, name):

    # Guardar nome do ficheiro
    filename = 'solved/' + name

    for i in range(height):
        for j in range(width):
            # Caso seja o caminho colocar pixel a vermelho
            if(matrix[i][j] == -1):
                rgb_im.putpixel((j, i), (255,0,0))

    rgb_im.save(filename)


if __name__ == "__main__":
    main()
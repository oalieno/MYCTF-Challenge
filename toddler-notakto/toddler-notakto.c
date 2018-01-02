#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define EMPTY_BOARD "\x01\x01\x01\x01\x01\x01\x01\x01\x01"

typedef char bool;

typedef struct Board {
    bool grid[3][3];
} Board;

Board board;

void board_init(Board * board, const char * stones) {
    for(int i = 0; i < 3; i++) for(int j = 0; j < 3; j++) {
        board->grid[i][j] = stones[i * 3 + j];
    }
}

void board_print(Board * board) {
    for(int i = 0; i < 3; i++) for(int j = 0; j < 3; j++) {
        if(board->grid[i][j] == 0) board->grid[i][j] = 'X';
        if(board->grid[i][j] == 1) board->grid[i][j] = ' ';
    }

    printf("\n");
    printf(" %c | %c | %c\n", board->grid[0][0], board->grid[0][1], board->grid[0][2]);
    printf("---+---+---\n");
    printf(" %c | %c | %c\n", board->grid[1][0], board->grid[1][1], board->grid[1][2]);
    printf("---+---+---\n");
    printf(" %c | %c | %c\n", board->grid[2][0], board->grid[2][1], board->grid[2][2]);
    printf("\n");
    
    for(int i = 0; i < 3; i++) for(int j = 0; j < 3; j++) {
        if(board->grid[i][j] == 'X') board->grid[i][j] = 0;
        if(board->grid[i][j] == ' ') board->grid[i][j] = 1;
    }
}

void board_move(Board * board, long long x, long long y) {
    board->grid[x][y] = 0;
}

void board_move_random(Board * board) {
    for(int i = 0; i < 3; i++) for(int j = 0; j < 3; j++) {
        if(board->grid[i][j]) {
            board->grid[i][j] = 0;
            return;
        }
    }
}

bool is_finish(Board * board) {
    for(int i = 0; i < 3; i++) {
        if(!board->grid[i][0] && !board->grid[i][1] && !board->grid[i][2]) return 1;
        if(!board->grid[0][i] && !board->grid[1][i] && !board->grid[2][i]) return 1;
    }

    if(!board->grid[0][0] && !board->grid[1][1] && !board->grid[2][2]) return 1;
    if(!board->grid[0][2] && !board->grid[1][1] && !board->grid[2][0]) return 1;

    return 0;
}

int main() {
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 2, 0LL);

    printf("========== Welcome to the Notakto Game ==========\n");
    printf("Notakto is tic-tac-toe with both players playing the same piece ( an 'X' )\n");
    printf("The player who end the game will LOSE THE GAME\n");
    
    Board example_board; board_init(&example_board, "012345678");
    board_print(&example_board);

    char name[10];
    printf("What's your name: ");
    read(0, name, 40);
    printf("Hello %s\n", name);

    while(1) {
        printf("========== A new round ==========\n");
        board_init(&board, EMPTY_BOARD);
        
        while(1) {
            printf("Your move: ");
            long long move; scanf("%lld", &move);
            long long x = move / 3, y = move % 3;
            
            board_move(&board, x, y);
            board_print(&board);
            if(is_finish(&board)) {
                printf("YOU LOSE\n");
                break;
            }

            board_move_random(&board);
            board_print(&board);
            if(is_finish(&board)) {
                printf("YOU WIN\n");
                break;
            }
        }
        
        while(1) {
            char choice;
            printf("Do you want to continue ( Y, N ) ? ");
            scanf("%c", &choice);
            if(choice != 'Y') printf("But I want to play again, please Q_Q\n");
            else break;
        }
    }

    return 0;
}

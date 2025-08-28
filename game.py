import random

def game():
    choices = ["kéo", "búa", "bao"]
    print("=== Trò chơi Kéo – Búa – Bao ===")
    print("Nhập: kéo / búa / bao")

    player = input("Bạn chọn: ").lower().strip()
    if player not in choices:
        print("Lựa chọn không hợp lệ!")
        return
    
    computer = random.choice(choices)
    print(f"Máy chọn: {computer}")

    if player == computer:
        print("Kết quả: Hòa 🤝")
    elif (player == "kéo" and computer == "bao") or \
         (player == "búa" and computer == "kéo") or \
         (player == "bao" and computer == "búa"):
        print("Bạn THẮNG 🎉")
    else:
        print("Bạn THUA 😢")

if __name__ == "__main__":
    while True:
        game()
        again = input("Chơi tiếp? (y/n): ").lower().strip()
        if again != "y":
            print("Cảm ơn bạn đã chơi!")
            break

# 🧩 A* Puzzle Game

Ứng dụng trò chơi xếp hình (N-Puzzle) sử dụng thuật toán A* để giải bài toán tự động, được phát triển cho môn học Trí tuệ nhân tạo.

## 📌 Giới thiệu

Đề tài xây dựng một trò chơi xếp hình có khả năng:

- Cho phép người dùng chơi puzzle thủ công
- Hỗ trợ AI giải tự động bằng thuật toán A*
- So sánh thuật toán A* với Greedy Best-First Search
- So sánh hiệu quả các hàm heuristic khác nhau
- Hiển thị trực quan quá trình giải thuật

Project được phát triển bằng Python với giao diện GUI trực quan.

---

## 🚀 Công nghệ sử dụng

- Python
- Tkinter
- Pygame
- Heapq
- Threading

---

## 🧠 Thuật toán sử dụng

### A* Search
Thuật toán tìm kiếm heuristic giúp tìm lời giải tối ưu.

Công thức đánh giá:

f(n) = g(n) + h(n)

Trong đó:

- `g(n)`: chi phí từ trạng thái đầu đến trạng thái hiện tại
- `h(n)`: heuristic ước lượng đến đích

### Greedy Best-First Search
Thuật toán tìm kiếm tham lam chỉ dựa vào heuristic.

---

## 📊 Các heuristic được hỗ trợ

### Manhattan Distance
- Tổng khoảng cách hàng và cột
- Cho hiệu quả tốt nhất

### Misplaced Tiles
- Đếm số ô sai vị trí

### Tiles Out of Row/Column
- Đếm số ô sai hàng hoặc cột

---

## 🎮 Chức năng chính

### ✅ Chơi puzzle thủ công
- Hỗ trợ:
  - 3x3
  - 4x4
  - 5x5

### ✅ AI Support
- Giải tự động bằng A*

### ✅ Compare AI
So sánh:
- A*
- Greedy Best-First Search

Hiển thị:
- Thời gian thực thi
- Số bước
- Số nút duyệt

### ✅ Compare Heuristic
So sánh hiệu quả các heuristic khác nhau.

### ✅ Chọn ảnh tùy chỉnh
Người dùng có thể chọn ảnh từ máy tính để tạo puzzle.

---

## 🖥️ Giao diện hệ thống

### Start Screen
- Start
- Compare AI
- Exit

### Game Screen
- Timer
- Steps Counter
- Support AI
- Heuristic Compare
- Upload Image

### Compare Screen
Hiển thị trực quan quá trình giải giữa:
- A*
- Greedy Best-First Search

---

## 📂 Cấu trúc project

```bash
project/
│
├── main.py
├── start_screen.py
├── level_screen.py
├── game_screen.py
├── compare_screen.py
├── assets/
│   ├── images/
│   └── sounds/
├── algorithms/
│   ├── astar.py
│   ├── greedy.py
│   └── heuristics.py
└── README.md
```

---

## ⚙️ Cài đặt

### 1. Clone repository

```bash
git clone <your-repository-link>
cd <repository-name>
```

### 2. Cài thư viện

```bash
pip install pygame
```

### 3. Chạy chương trình

```bash
python main.py
```

---

## 📈 Kết quả thực nghiệm

| Thuật toán | Thời gian | Số bước | Số nút duyệt |
|---|---|---|---|
| A* | 0.43s | 31 | 20451 |
| Greedy | 0.003s | 47 | 101 |

### Kết luận
- A* cho lời giải tối ưu hơn
- Greedy nhanh hơn nhưng không đảm bảo đường đi ngắn nhất

---

## 🎯 Mục tiêu đồ án

- Minh họa trực quan thuật toán A*
- Giúp người học hiểu heuristic trong AI
- Ứng dụng AI vào trò chơi puzzle

---

## 🔮 Hướng phát triển

- Hỗ trợ puzzle lớn hơn (6x6, 7x7)
- Tối ưu hiệu năng
- Thêm nhiều thuật toán tìm kiếm
- Multiplayer mode
- Reinforcement Learning

---

## 👨‍💻 Thành viên nhóm

- Nguyễn Phúc An – 23110175
- Trần Nguyễn Castrol – 23110185
- Trần Quang Duy – 23110195

Giảng viên hướng dẫn:
- TS. Bùi Mạnh Quân

---

## 📚 Tài liệu tham khảo

- Artificial Intelligence
- A* Search Algorithm
- Pygame Documentation
- Python Documentation

---

## 📄 License

Dự án phục vụ mục đích học tập và nghiên cứu.

### **📌 C 语言 `struct` 结构体详解**
C 语言的 **`struct` 结构体**（structure）是一种**自定义数据类型**，用于存储**多个不同类型的变量**，可以让程序更加**模块化、结构化**。

---

## **1️⃣ `struct` 结构体的基本定义**
```c
#include <stdio.h>

// **定义结构体**
struct Student {
    char name[50];   // 姓名
    int age;         // 年龄
    float score;     // 成绩
};

int main() {
    struct Student s1 = {"Alice", 20, 95.5};  // 定义结构体变量并初始化

    // **访问结构体成员**
    printf("姓名: %s\n", s1.name);
    printf("年龄: %d\n", s1.age);
    printf("成绩: %.1f\n", s1.score);

    return 0;
}
```
📌 **说明**：
- **`struct Student`** 定义了一个**包含 `name`、`age`、`score` 的结构体**。
- **`struct Student s1 = {...}`** 创建并初始化结构体变量 `s1`。
- **使用 `s1.name`、`s1.age` 访问结构体成员**。

---

## **2️⃣ 结构体数组**
📌 **可以使用结构体数组存储多个学生的信息**：
```c
#include <stdio.h>

struct Student {
    char name[50];
    int age;
    float score;
};

int main() {
    struct Student students[3] = { 
        {"Alice", 20, 95.5}, 
        {"Bob", 21, 88.0}, 
        {"Charlie", 22, 78.5} 
    };

    // **遍历结构体数组**
    for (int i = 0; i < 3; i++) {
        printf("学生%d: 姓名=%s, 年龄=%d, 成绩=%.1f\n", i+1, students[i].name, students[i].age, students[i].score);
    }

    return 0;
}
```
📌 **说明**：
- **定义结构体数组 `students[3]`**，存储多个学生信息。
- **使用 `for` 循环遍历 `students[i]`，访问成员 `name, age, score`**。

---

## **3️⃣ 结构体指针**
📌 **可以用指针访问结构体成员**：
```c
#include <stdio.h>

struct Student {
    char name[50];
    int age;
    float score;
};

int main() {
    struct Student s1 = {"Alice", 20, 95.5};
    struct Student *p = &s1;  // 定义指向结构体的指针

    // **通过指针访问结构体成员**
    printf("姓名: %s\n", p->name);  // 等价于 (*p).name
    printf("年龄: %d\n", p->age);
    printf("成绩: %.1f\n", p->score);

    return 0;
}
```
📌 **说明**：
- **`struct Student *p = &s1;`** 让 `p` 指向 `s1` 结构体变量的地址。
- **使用 `p->name` 访问结构体成员**（等价于 `(*p).name`）。
- **结构体指针适用于动态分配结构体变量**。

---

## **4️⃣ 结构体作为函数参数**
📌 **结构体可以作为函数参数传递**：
```c
#include <stdio.h>

struct Student {
    char name[50];
    int age;
    float score;
};

// **传递结构体变量**
void printStudent(struct Student s) {
    printf("姓名: %s, 年龄: %d, 成绩: %.1f\n", s.name, s.age, s.score);
}

int main() {
    struct Student s1 = {"Alice", 20, 95.5};
    printStudent(s1);  // 传递结构体变量

    return 0;
}
```
📌 **说明**：
- 结构体作为参数 **按值传递**，不会改变原变量值。

🔹 **如果要在函数中修改结构体变量**，应**使用指针传递**：
```c
void modifyStudent(struct Student *s) {
    s->age += 1;  // 修改成员
}

int main() {
    struct Student s1 = {"Alice", 20, 95.5};
    modifyStudent(&s1);
    printf("修改后年龄: %d\n", s1.age);  // 21
}
```

---

## **5️⃣ `typedef` 简化结构体声明**
📌 **使用 `typedef` 为结构体取别名，简化使用**：
```c
#include <stdio.h>

// **使用 typedef 给结构体取别名**
typedef struct {
    char name[50];
    int age;
    float score;
} Student;  // 直接用 `Student` 代替 `struct Student`

int main() {
    Student s1 = {"Alice", 20, 95.5};  // 直接使用 Student
    printf("姓名: %s, 年龄: %d, 成绩: %.1f\n", s1.name, s1.age, s1.score);

    return 0;
}
```
📌 **说明**：
- **`typedef struct {...} Student;`** 让 `Student` 代替 `struct Student`，代码更简洁。
- **可以直接 `Student s1;`，而不用 `struct Student s1;`**。

---

## **6️⃣ 结构体嵌套**
📌 **结构体可以嵌套，即一个结构体可以包含另一个结构体**：
```c
#include <stdio.h>

typedef struct {
    char street[50];
    char city[50];
} Address;

typedef struct {
    char name[50];
    int age;
    Address addr;  // **嵌套结构体**
} Student;

int main() {
    Student s1 = {"Alice", 20, {"123 Main St", "New York"}};

    printf("姓名: %s, 年龄: %d\n", s1.name, s1.age);
    printf("地址: %s, %s\n", s1.addr.street, s1.addr.city);

    return 0;
}
```
📌 **说明**：
- `Student` 结构体 **嵌套 `Address` 结构体**，可以直接访问 `s1.addr.street`。

---

## **7️⃣ 结构体与动态内存分配**
📌 **可以使用 `malloc()` 动态分配结构体内存**：
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    int age;
} Student;

int main() {
    // **动态分配结构体内存**
    Student *s = (Student *)malloc(sizeof(Student));

    if (s == NULL) {
        printf("内存分配失败！\n");
        return 1;
    }

    // **赋值**
    s->age = 20;
    strcpy(s->name, "Alice");

    // **访问结构体成员**
    printf("姓名: %s, 年龄: %d\n", s->name, s->age);

    free(s);  // **释放内存**
    return 0;
}
```
📌 **说明**：
- `malloc(sizeof(Student))` **动态分配结构体内存**。
- **必须 `free(s);` 释放内存，防止内存泄漏！**

---

## **📌 总结**
| **结构体特性** | **代码示例** | **说明** |
|--------------|------------|---------|
| **定义结构体** | `struct Student {...};` | 存储多个不同类型的变量 |
| **结构体变量** | `struct Student s1 = {...};` | 直接使用结构体变量 |
| **结构体数组** | `struct Student students[10];` | 存储多个结构体数据 |
| **结构体指针** | `struct Student *p = &s1;` | 用 `->` 访问成员 |
| **结构体作为函数参数** | `void func(struct Student s);` | **按值传递** |
| **使用 `typedef`** | `typedef struct {...} Student;` | 简化 `struct` 关键字 |
| **嵌套结构体** | `struct A { struct B b; };` | 结构体包含另一个结构体 |
| **动态分配结构体** | `Student *s = (Student *)malloc(sizeof(Student));` | **需要 `free()` 释放内存** |

✅ **掌握 `struct`，让你的 C 语言代码更清晰、更强大！🚀**
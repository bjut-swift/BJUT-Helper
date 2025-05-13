## **`fgets()` 函数总结**

### **1. `fgets()` 的基本用法**
`fgets()` 用于 **从标准输入 (`stdin`) 或文件读取字符串**，并确保不会超出缓冲区大小。  
```c
char *fgets(char *str, int size, FILE *stream);
```
- `str`：目标字符数组（存储输入的字符串）。
- `size`：**最多读取 `size-1` 个字符**，最后自动加 `\0` 终止符。
- `stream`：输入流，通常为 `stdin`（标准输入）。

---

### **2. `fgets()` 读取用户输入**
```c
#include <stdio.h>

int main() {
    char str[50];  // 定义字符数组

    printf("请输入一句话: ");
    fgets(str, sizeof(str), stdin);  // 读取输入

    printf("你输入的是: %s", str);  // 输出字符串
    return 0;
}
```
#### **示例输入**
```
Hello, C programming!
```
#### **示例输出**
```
你输入的是: Hello, C programming!
```
> **注意**：`fgets()` **会保留换行符 `\n`**（如果缓冲区足够大）。

---

### **3. `fgets()` 的换行符问题**
如果输入内容不足 `size-1`，且按下 `Enter`，`fgets()` **会将 `\n` 存入 `str`**：
```c
#include <stdio.h>

int main() {
    char str[10];

    printf("请输入: ");
    fgets(str, sizeof(str), stdin);

    printf("你输入的是: %s", str);  // 可能包含换行符
    return 0;
}
```
#### **示例输入**
```
Hello
```
#### **示例输出**
```
你输入的是: Hello
（光标换行）
```
> 由于 `Hello` 只有 5 个字符，`\n` 也被存入 `str`，所以输出后换行。

#### **去除换行符**
```c
#include <stdio.h>
#include <string.h>

int main() {
    char str[50];

    printf("请输入: ");
    fgets(str, sizeof(str), stdin);

    // 查找换行符并替换为字符串结束符
    str[strcspn(str, "\n")] = '\0';

    printf("你输入的是: %s", str);
    return 0;
}
```

---

### **4. `sizeof(str)` 在 `fgets()` 中的作用**
```c
char str[50];
fgets(str, sizeof(str), stdin);  // 确保不会超出 50 字节
```
✅ **优点**：
- 避免 **缓冲区溢出**，安全读取输入。
- **可维护性高**，数组大小变化时无需修改代码。

⚠️ **错误示例（不适用于指针）**
```c
char *str;
fgets(str, sizeof(str), stdin);  // ❌ 错误，str 是指针，sizeof(str) 只是指针大小！
```
正确做法：
```c
char str[50];  // 使用字符数组
fgets(str, sizeof(str), stdin);
```

---

### **5. `fgets()` vs `scanf()`**
| **函数**   | **特点** | **能否读取空格** | **安全性** |
|------------|---------|----------------|------------|
| `scanf()`  | 读取单词，遇到空格停止 | ❌ 否 | 可能导致缓冲区溢出 |
| `fgets()`  | 读取整行，包括空格 | ✅ 是 | **安全（限制最大长度）** |

#### **对比示例**
```c
#include <stdio.h>

int main() {
    char name1[20], name2[20];

    printf("使用 scanf 请输入姓名: ");
    scanf("%s", name1);  // 不能读取空格，遇到空格停止

    getchar();  // 清除缓冲区中的 `\n`

    printf("使用 fgets 请输入姓名: ");
    fgets(name2, sizeof(name2), stdin);  // 能读取空格

    printf("scanf 输入: %s\n", name1);
    printf("fgets 输入: %s", name2);  // 可能包含换行符
    return 0;
}
```
#### **示例输入**
```
使用 scanf 请输入姓名: John Doe
使用 fgets 请输入姓名: Alice Smith
```
#### **示例输出**
```
scanf 输入: John
fgets 输入: Alice Smith
```
> `scanf()` **遇到空格停止**，`fgets()` **能读取整行**。

---

### **6. `fgets()` 读取文件**
```c
#include <stdio.h>

int main() {
    FILE *fp = fopen("test.txt", "r");  // 以只读模式打开文件
    if (fp == NULL) {
        printf("文件打开失败\n");
        return 1;
    }

    char line[100];
    while (fgets(line, sizeof(line), fp)) {  // 逐行读取
        printf("%s", line);
    }

    fclose(fp);
    return 0;
}
```

---

### **7. 总结**
✅ **推荐使用 `fgets()` 读取字符串**，因为：
- **可以读取整行，支持空格**
- **安全（限制最大长度，防止缓冲区溢出）**
- **适用于标准输入 `stdin` 和文件**

🚀 **最佳实践**
```c
fgets(str, sizeof(str), stdin);
str[strcspn(str, "\n")] = '\0';  // 去掉换行符
```
这样代码既 **安全**，又 **易维护**！🎯
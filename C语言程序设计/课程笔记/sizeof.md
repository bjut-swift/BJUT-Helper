### **`sizeof` 运算符**
`sizeof` 是 **C 语言的关键字**，用于计算**变量、数据类型或数组**的**字节大小**。

---

## **1. `sizeof` 的基本用法**
**语法：**
```c
sizeof(数据类型)
sizeof(变量)
sizeof(数组)
```
- `sizeof(类型)` **返回该类型的大小（字节数）**
- `sizeof(变量)` **返回变量占用的字节数**
- `sizeof(数组)` **返回整个数组的总大小（所有元素的大小总和）**

---

## **2. `sizeof` 的应用示例**
### **（1）计算基本数据类型的大小**
```c
#include <stdio.h>

int main() {
    printf("char: %lu 字节\n", sizeof(char));
    printf("int: %lu 字节\n", sizeof(int));
    printf("float: %lu 字节\n", sizeof(float));
    printf("double: %lu 字节\n", sizeof(double));
    return 0;
}
```
📌 **示例输出（不同系统可能不同）：**
```
char: 1 字节
int: 4 字节
float: 4 字节
double: 8 字节
```

---

### **（2）计算变量的大小**
```c
#include <stdio.h>

int main() {
    int a = 10;
    char b = 'A';
    double c = 3.14;

    printf("a 占 %lu 字节\n", sizeof(a));
    printf("b 占 %lu 字节\n", sizeof(b));
    printf("c 占 %lu 字节\n", sizeof(c));

    return 0;
}
```

---

### **（3）计算数组的大小**
```c
#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5};

    printf("数组总大小: %lu 字节\n", sizeof(arr));
    printf("数组元素个数: %lu\n", sizeof(arr) / sizeof(arr[0]));
    printf("每个元素大小: %lu 字节\n", sizeof(arr[0]));

    return 0;
}
```
📌 **示例输出（假设 `int` 占 4 字节）：**
```
数组总大小: 20 字节
数组元素个数: 5
每个元素大小: 4 字节
```
📌 **计算数组长度：**
```c
int n = sizeof(arr) / sizeof(arr[0]);  // 计算数组的元素个数
```

---

## **3. `sizeof` 与指针**
### **（1）指针的 `sizeof`**
```c
#include <stdio.h>

int main() {
    int *p;
    double *q;

    printf("指针 p 的大小: %lu 字节\n", sizeof(p)); 
    printf("指针 q 的大小: %lu 字节\n", sizeof(q));

    return 0;
}
```
📌 **指针大小一般为 4 或 8 字节（取决于系统架构）**
```
指针 p 的大小: 8 字节
指针 q 的大小: 8 字节
```
💡 **注意：**
- `sizeof(指针变量)` 返回**指针本身的大小**，而不是指向数据的大小！
- 例如 `sizeof(int*)` 在 64 位系统上通常为 **8**，但 `sizeof(int)` 仍然是 **4**。

---

### **（2）`sizeof` 不能用于计算指针指向的数组大小**
```c
#include <stdio.h>

void func(int arr[]) {
    printf("sizeof(arr) = %lu\n", sizeof(arr));  // ⚠️ 这里 `arr` 只是指针
}

int main() {
    int arr[10];
    printf("sizeof(arr) = %lu\n", sizeof(arr));  // 正确：计算整个数组大小

    func(arr);  // 传递给函数后，`arr` 退化为指针

    return 0;
}
```
📌 **示例输出（假设 `int` 占 4 字节）：**
```
sizeof(arr) = 40  // 10 * 4 = 40
sizeof(arr) = 8   // 退化为指针，指针大小为 8
```
✅ **解决方案**：手动传递数组长度：
```c
void func(int arr[], int size) {  // 传递数组长度
    printf("数组长度: %d\n", size);
}
```

---

## **4. `sizeof` 的注意事项**
| **常见问题** | **正确使用方式** |
|--------------|----------------|
| `sizeof(数组)` 获取数组总大小 | **只能用于局部数组，指针不行** |
| `sizeof(指针)` 计算的是**指针本身**的大小，而不是指向的数组 | 使用 `sizeof(arr) / sizeof(arr[0])` 计算数组元素个数 |
| 计算字符串长度时，`sizeof(str)` 包含 `\0`，但 `strlen(str)` 不包含 | 计算字符串长度用 `strlen(str)` |
| `sizeof` 是编译时计算的，适用于静态数组 | **动态分配的数组不能用 `sizeof` 获取元素个数** |

---

## **总结**
| 用法 | 示例 | 说明 |
|------|------|------|
| 计算数据类型大小 | `sizeof(int)` | 获取 `int` 类型的字节大小 |
| 计算变量大小 | `sizeof(a)` | 获取变量 `a` 所占的字节数 |
| 计算数组大小 | `sizeof(arr)` | 获取整个数组的总大小 |
| 计算数组长度 | `sizeof(arr) / sizeof(arr[0])` | 计算数组的元素个数 |
| 计算指针大小 | `sizeof(p)` | 计算指针变量的大小 |
| **指针传递时 `sizeof` 失效** | **数组作为参数会退化为指针** | 需要手动传递数组长度 |

✅ `sizeof` 在**计算数组大小、数据类型大小**时非常有用，但在**指针**上要小心！🚀
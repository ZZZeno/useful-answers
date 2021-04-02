为什么golang里不能把 []int 类型变量传递给函数 func ([]interface{ })
golang不支持协变，int实现了[]interface，并不一定使[]int实现了[]interface，如果真的需要做，在传参之前需要进行类型转换

https://studygolang.com/articles/13383

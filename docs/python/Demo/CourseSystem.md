# 课程系统

## 需求分析（课程与班级合为一体）

1. 管理视图

    1. 注册
    2. 登录
    3. 创建学校
    4. 创建课程（先选择学校）
    5. 创建讲师

2. 学员视图

    1. 注册
    2. 登录功能
    3. 选择校区
    4. 选择课程（先选择校区，在选择校区中的某一门课程）
        * 学生选择课程，课程也选择学生
    5. 查看分数

3. 讲师视图

    1. 登录
    2. 查看教授课程
    3. 选择教授课程
    4. 查看课程下的学生
    5. 修改学生分数

上述操作所产生的数据通过pickle保存到文件。


## 程序架构设计（三层架构）

* 用户视图层
    * 用于与用户进行交互
    * 简单的逻辑判断，比如注册功能中两次密码是否一致的校验
    * core
        * src.py 主视图
        * admin.py: admin_view
        * student.py: student_view
        * teacher.py: teacher_view
* 逻辑接口层
    * 核心业务逻辑的处理
    * interface
        * admin_interface.py
        * studeng_interface.py
        * teacher_interface.py
* 数据处理层
    * 数据处理，比如增删改查。
    * db
        * models.py
        * db_handler.py
            * ATM + 购物车
                * 存放json格式的数据
                * dict --> json
        * 选课系统(******)    
            * pickle保存对象
            * object --> pickle

## 文件结构：

    /--conf/
    |    |--settings.py
    |
    |--core/
    |    |--src.py
    |    |--admin.py
    |    |--student.py
    |    |--teacher.py
    |
    |--db/
    |    |--models.py
    |    |--db_handler.py
    |        |--pickle
    |
    |--interface/
    |    |--admin_interface.py
    |    |--student_interface.py
    |    |--teacher_interface.py
    |
    |--lib/
    |    |--common.py
    |
    |--readme.md
    |
    |--start.py



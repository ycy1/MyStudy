abstract class Person {
  String name = "";
  int age = 0;

  void printInfo();
}

class Doctor implements Person {
  String name = "";
  int age = 0;

  // Doctor(this.name, this.age);

  @override
  void printInfo() {
    print("Doctor: name：$name, age：$age");
  }
}

mixin MyMixin {
  void mixFunc(String name) {
    print("mixFunc: $name");
  }
}

mixin MyMixin2 {
  void mixFunc2(String name) {
    print("mixFunc2: $name");
  }
}

class Student with MyMixin, MyMixin2 {
  String name = "";
  int age = 0;
  String info = "";

  Student(this.name, this.age);
  Student.create(this.name, this.age) {
    if (age > 18) {
      this.info = "成年";
    } else {
      this.info = "未成年";
    }
  }

  void _printInfo() {
    print("name：$name, age：$age, info：$info");
  }

  void printInfo() {
    print("访问私有方法");
    _printInfo();
  }

  void func() {
    print("func");
  }
}

class Teacher extends Student with MyMixin, MyMixin2 {
  String className = "math";

  Teacher(String name, int age) : super(name, age) {
    className = "math";
  }

  @override
  void printInfo() {
    // super._printInfo(); // 调用父类的私有方法
    print("name：$name, age：$age, className：$className");
  }
}

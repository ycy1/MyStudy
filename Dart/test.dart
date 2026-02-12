import "./classTest.dart";

void main(List<String> args) {
  print("Hello World! dart\n");
  // var age = 18;
  // age = 19;
  // age = int.parse("5");
  // print(age);

  // const name = "1.2";
  // // name = "flutter";
  // print(name);

  // final height = 1.75;
  // // const time = DateTime.now(); // 编译时确定
  // final time2 = DateTime.now(); // 运行时确定

  // print(time2);

  String name2 = "flutter ${DateTime.now()}";
  // print(name2.toUpperCase());

  int add(int a, int b, {int? d, int e = 4}) {
    return a + b + (d ?? 0) + e;
  }

  int sum = add(2, 5, d: null);
  // print("sum：$sum");

  // Student student = Student("flutter", 18);
  Student student2 = Student.create("张三", 10);
  // student.name = "张三";
  // student.age = 18;
  // student.printInfo();
  // student2.printInfo();
  // student2.mixFunc(student2.name);
  // student2.mixFunc2(student2.name);

  Teacher teacher = Teacher("李四", 30);
  // teacher.printInfo();
  // teacher.func();
  // teacher.mixFunc(teacher.name);
  // teacher.mixFunc2(teacher.name);

  // Doctor doctor = Doctor();
  // doctor.name = "李四";
  // doctor.age = 30;
  // doctor.printInfo();

  // Person person = Doctor();
  // person.name = "李四";
  // person.age = 30;
  // person.printInfo();

  Map<T, String> getValue<T, M>(T key, M value2) {
    // print(value2.runtimeType);
    // print(value2 is Student);
    // print(assert(value2 is Student)); // 断言 obj 是
    // assert(value2 is Student);
    if (value2 is Student) {
      // 类型提升
      // print(value2.name);
      return {key: value2.name};
    }
    return {key: value2.toString()};
  }

  // print(getValue<int, Student>(10, student2));
  // print(getValue<String>("flutter"));
  // print(getValue<double>(3.14));

  // Future f = Future(() {
  //   // throw "抛出错误";
  //   return "hello world";
  // });
  // f
  //     .then((value) {
  //       print(value);
  //       return Future(() => "hello flutter");
  //     })
  //     .then((value) {
  //       print(value);
  //       return Future(() {
  //         throw "抛出错误2";
  //         // return "aa";
  //       });
  //     })
  //     .then((value) => print(value))
  //     .catchError((error) => print(error))
  //     .whenComplete(() => print("完成"));

  // f.catchError((error) {
  //   print(error);
  // });
  // f.whenComplete(() {
  //   print("完成");
  // });

  void test() async {
    try {
      var result = await Future(() async {
        await Future.delayed(Duration(seconds: 2));
        // throw "抛出错误";
        return "hello flutter";
      });
      print(result);
    } catch (e) {
      print(e);
    } finally {
      print("finally");
    }
  }

  test();
}

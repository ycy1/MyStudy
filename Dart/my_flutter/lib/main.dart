import 'package:flutter/material.dart';
import 'package:flutter/widget_previews.dart';
import 'package:logger/logger.dart';

// final logger = Logger();
final Logger logger = Logger(
  // printer: PrettyPrinter(
  //   methodCount: 0, // 不显示方法调用栈
  //   errorMethodCount: 8, // 错误时显示8层栈信息
  //   lineLength: 120,
  //   colors: true,
  //   printEmojis: true,
  //   printTime: false,
  // ),
  printer: SimplePrinter(colors: true),
  // 或者使用简单的控制台输出
  // printer: SimplePrinter(colors: true),
);

void main(List<String> args) {
  // runApp(mainPage());
  runApp(UseStatePage());
}

// 无状态主页面
class mainPage extends StatelessWidget {
  const mainPage({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Hello My Flutter')),
        body: Center(child: Text('Hello mainPage')),
        bottomNavigationBar: BottomNavigationBar(
          items: [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
            BottomNavigationBarItem(
              icon: Icon(Icons.business),
              label: 'Business',
            ),
            BottomNavigationBarItem(icon: Icon(Icons.school), label: 'School'),
          ],
        ),
        floatingActionButton: FloatingActionButton(
          child: Icon(Icons.add),
          onPressed: () {
            print('add pressed');
          },
        ),
      ),
    );
  }
}

class ChildPage extends StatelessWidget {
  final String? param;
  final Function(String?) onParamChange;
  const ChildPage({super.key, this.param, required this.onParamChange});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Container(
      child: TextButton(
        child: Text('子组件$param'),
        onPressed: () {
          onParamChange('hello parent');
        },
      ),
    );
  }
}

class UseStateChildPage extends StatefulWidget {
  // @Preview(size: Size(300, 800))
  final String? param;
  final Function(String?) onParamChange;
  const UseStateChildPage({super.key, this.param, required this.onParamChange});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _UseStateChildPageState();
  }
}

class _UseStateChildPageState extends State<UseStateChildPage> {
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Container(
      child: TextButton(
        child: Text('子组件${widget.param}'),
        onPressed: () {
          widget.onParamChange('hello state parent');
        },
      ),
    );
  }
}

// createState -> initState -> didChangeDependencies -> build
// 路由切换时会调用 deactivate -> dispose
class UseStatePage extends StatefulWidget {
  @Preview(size: Size(300, 800))
  const UseStatePage({super.key});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _UseStatePageState();
  }
}

// 有状态页面
class _UseStatePageState extends State<UseStatePage> {
  late ScrollController _scrollController;

  @override
  void initState() {
    // TODO: implement initState
    debugPrint('initState');
    _scrollController = ScrollController();
    super.initState();
    // 添加滚动监听
    // _scrollController.addListener(() {
    //   debugPrint("当前滚动位置: ${_scrollController.offset}");
    // });
  }

  @override
  didChangeDependencies() {
    // TODO: implement didChangeDependencies
    debugPrint('didChangeDependencies');
    super.didChangeDependencies();
  }

  @override
  didUpdateWidget(oldWidget) {
    // TODO: implement didUpdateWidget
    debugPrint('didUpdateWidget');
    super.didUpdateWidget(oldWidget);
  }

  @override
  deactivate() {
    // TODO: implement deactivate
    debugPrint('deactivate');
    super.deactivate();
  }

  @override
  void dispose() {
    // TODO: implement dispose
    debugPrint('dispose');
    _scrollController.dispose(); // 重要：释放控制器
    super.dispose();
  }

  //   # 1. 按 Ctrl+Shift+P
  //   # 2. 输入 "Flutter: Hot Restart"
  double get _spacing_w => MediaQuery.of(context).size.width;
  double get _spacing_h => MediaQuery.of(context).size.height;
  int count = 0;
  final bool _isVisible = false;
  List<Widget> getContainers() {
    return List.generate(
      10,
      (index) => Container(width: 50, height: 50, color: Colors.green),
    );
  }

  List<Widget> getTexts() {
    return List.generate(
      3,
      (index) => Row(
        // mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            flex: 5,
            child: AspectRatio(
              aspectRatio: 0.8,
              child: Image.network(
                width: double.infinity,
                'http://182.92.85.80/group1/M00/00/05/tlxVUGj9wDeAQw_wAAB0SNogJnk18.webp',
                fit: BoxFit.cover,
              ),
            ),
          ),
          SizedBox(width: _spacing_w * 0.02), // 屏幕宽度的2%
          Expanded(
            flex: 5,
            child: AspectRatio(
              aspectRatio: 0.8,
              child: Image.asset(
                'images/github.jpg',
                width: double.infinity,
                // height: 200,
                fit: BoxFit.cover,
              ),
            ),
          ),
        ],
      ),
    );
  }

  final TextEditingController _textController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    // logger.d(context.widget.runtimeType);
    debugPrint('build');
    debugPrint(_isVisible.toString());
    // debugPrint(context.widget.runtimeType.toString()); // debugPrint 在生产环境会自动被禁用

    // TODO: implement build
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Hello My Flutter')),
        body: Scrollbar(
          controller: _scrollController,
          child: SingleChildScrollView(
            controller: _scrollController, // 这里也需要添加控制器
            child: Container(
              // height: 800,
              margin: EdgeInsets.all(10),
              child: Padding(
                padding: EdgeInsets.all(0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    Container(
                      transform: Matrix4.rotationZ(0.05),
                      width: 150,
                      height: 150,
                      margin: EdgeInsets.only(bottom: 20),
                      decoration: BoxDecoration(
                        color: Colors.blue,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: Colors.amber, width: 3),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.amber,
                            offset: Offset(4, 2),
                            blurRadius: 4,
                          ),
                        ],
                      ),
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text.rich(
                              TextSpan(
                                text: '',
                                children: [
                                  TextSpan(text: 'Hello'),
                                  TextSpan(
                                    text: ' Flutter',
                                    style: TextStyle(color: Colors.red),
                                  ),
                                ],
                                style: TextStyle(
                                  color: Colors.deepPurple,
                                  fontSize: 20,
                                  fontStyle: FontStyle.italic,
                                  fontWeight: FontWeight.bold,
                                  decoration: TextDecoration.underline,
                                  decorationColor: Colors.amber,
                                ),
                              ),
                            ),
                            // Text(
                            //   'Hello UseStatePage UseStatePage UseStatePage',
                            //   maxLines: 1,
                            //   overflow: TextOverflow.ellipsis,
                            //   style: TextStyle(
                            //     color: Colors.white,
                            //     fontSize: 15,
                            //     fontStyle: FontStyle.italic,
                            //     fontWeight: FontWeight.bold,
                            //     decoration: TextDecoration.underline,
                            //     decorationColor: Colors.amber,
                            //   ),
                            // ),
                            Text(
                              'row column',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 15,
                              ),
                            ),
                            // Text(
                            //   'row column3',
                            //   style: TextStyle(color: Colors.white, fontSize: 20),
                            // ),
                          ],
                        ),
                      ),
                    ),
                    Flex(
                      direction: Axis.horizontal,
                      children: [
                        Expanded(
                          flex: 3,
                          child: Container(
                            width: 50,
                            height: 50,
                            color: const Color.fromRGBO(244, 67, 54, 1),
                          ),
                        ),
                        Expanded(
                          flex: 2,
                          child: Container(
                            width: 50,
                            height: 50,
                            color: Colors.green,
                          ),
                        ),
                        Expanded(
                          flex: 1,
                          child: Container(
                            width: 50,
                            height: 50,
                            color: Colors.cyan,
                          ),
                        ),
                      ],
                    ),
                    Wrap(
                      // alignment: WrapAlignment.center,
                      // direction: Axis.horizontal,
                      spacing: 25,
                      runSpacing: 10,
                      children: getContainers(),
                    ),
                    Stack(
                      alignment: Alignment.center,
                      children: [
                        Container(width: 150, height: 150, color: Colors.blue),
                        Container(width: 100, height: 100, color: Colors.red),
                        // Container(width: 50, height: 50, color: Colors.yellow),
                        Positioned(
                          top: 0,
                          // bottom: 0,
                          left: 10,
                          child: Container(
                            width: 50,
                            height: 50,
                            color: Colors.yellow,
                          ),
                        ),
                      ],
                    ),
                    Column(
                      // mainAxisAlignment: MainAxisAlignment.center,
                      // crossAxisAlignment: CrossAxisAlignment.start,
                      children: getTexts(),
                    ),
                    SizedBox(height: 20),
                    Column(
                      children: [
                        TextField(
                          // style: TextStyle(backgroundColor: Colors.amber),
                          controller: _textController,
                          onChanged: (value) => setState(() {
                            debugPrint(value);
                          }),
                          decoration: InputDecoration(
                            contentPadding: EdgeInsets.only(left: 20),
                            hintText: 'Enter your name',
                            hintStyle: TextStyle(
                              color: const Color.fromARGB(255, 136, 150, 225),
                            ),
                            filled: true,
                            // hintStyle: TextStyle(color: Colors.indigo),
                            fillColor: const Color.fromARGB(99, 50, 168, 223),
                            border: OutlineInputBorder(
                              borderSide: BorderSide.none,
                              borderRadius: BorderRadius.circular(20.0),
                            ),
                            // labelText: 'Enter your name',
                          ),
                        ),
                        SizedBox(height: 10),
                        TextField(
                          controller: _passwordController,
                          onChanged: (value) => setState(() {
                            debugPrint(value);
                          }),
                          obscureText: true,
                          // style: TextStyle(backgroundColor: Colors.amber),
                          decoration: InputDecoration(
                            contentPadding: EdgeInsets.only(left: 20),
                            hintText: 'Enter your password',
                            hintStyle: TextStyle(
                              color: const Color.fromARGB(255, 136, 150, 225),
                            ),
                            filled: true,
                            // hintStyle: TextStyle(color: Colors.indigo),
                            fillColor: const Color.fromARGB(99, 50, 168, 223),
                            border: OutlineInputBorder(
                              borderSide: BorderSide.none,
                              borderRadius: BorderRadius.circular(20.0),
                            ),
                            // labelText: 'Enter your name',
                          ),
                        ),
                        SizedBox(height: 10),
                        SizedBox(
                          width: double.infinity,
                          child: TextButton(
                            onPressed: () => debugPrint(
                              'name: ${_textController.text}, password: ${_passwordController.text}',
                            ),
                            style: TextButton.styleFrom(
                              backgroundColor: Colors.blueAccent,
                              foregroundColor: Colors.yellowAccent,
                              textStyle: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            child: Text('Login'),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 20),
                    Column(
                      children: [
                        Text('父组件'),
                        ChildPage(
                          param: 'hello no state',
                          onParamChange: (value) => debugPrint(value),
                        ),
                        UseStateChildPage(
                          param: 'hello state',
                          onParamChange: (value) => debugPrint(value),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
        bottomNavigationBar: BottomNavigationBar(
          items: [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
            BottomNavigationBarItem(
              icon: Icon(Icons.business),
              label: 'Business',
            ),
            BottomNavigationBarItem(icon: Icon(Icons.school), label: 'School'),
          ],
        ),

        floatingActionButton: _isVisible
            ? Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  FloatingActionButton(
                    child: Icon(Icons.add),
                    onPressed: () {
                      setState(() {
                        count++;
                      });
                    },
                  ),
                  Text('$count'),
                  FloatingActionButton(
                    child: Icon(Icons.arrow_upward),
                    onPressed: () {
                      setState(() {
                        count--;
                      });
                      // _scrollController.jumpTo(0);
                      _scrollController.animateTo(
                        0, // 目标位置
                        duration: Duration(milliseconds: 1000), // 动画时长
                        curve: Curves.easeInOut, // 动画曲线
                      );
                    },
                  ),
                ],
              )
            : null,
        floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      ),
    );
  }
}

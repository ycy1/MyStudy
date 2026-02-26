import 'package:flutter/material.dart';
import 'package:flutter/widget_previews.dart';
// import 'package:flutter/widget_previews.dart';

void main(List<String> args) {
  runApp(UseStatePage());
}

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

class _UseStatePageState extends State<UseStatePage> {
  // late ScrollController _singlechildScrollView = ScrollController();
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return MaterialApp(
      initialRoute: '/login',
      routes: {
        '/login': (context) => UseStatePageLogin(),
        '/home': (context) => UseStatePage(),
        // '/detail': (context) => UseStatePageDetail(title: "详情"),
      },
      onGenerateRoute: (settings) {
        print("settings:${settings.arguments}");

        var arguments = settings.arguments;
        // if (settings.name == '/detail' &&
        //     settings.arguments != null &&
        //     !(arguments as Map)["login"]) {
        //   return MaterialPageRoute(builder: (context) => UseStatePageLogin());
        // }
        print("arguments:${(arguments as Map)["index"]}");
        if (settings.name == '/detail' &&
            settings.arguments != null &&
            (((arguments as Map)["index"] as int) % 2 == 0)) {
          return MaterialPageRoute(builder: (context) => UseStatePageLogin());
        } else if (settings.name == '/detail') {
          return MaterialPageRoute(
            builder: (context) =>
                UseStatePageDetail(title: "详情${(arguments as Map)["index"]}"),
          );
        }
        // return MaterialPageRoute(builder: (context) => UseStatePageLogin());
      },
      onUnknownRoute: (settings) {
        debugPrint('onUnknownRoute:${settings}');
        return MaterialPageRoute(builder: (context) => UseStatePageNotFound());
      },
      home: Scaffold(
        body:
            // ListView.separated(
            //   separatorBuilder: (context, index) => SizedBox(height: 10),
            //   itemCount: 50,
            //   itemBuilder: (context, index) =>
            //       Container(child: Text('$index'), height: 50, color: Colors.green),
            //   // children: List.generate(
            //   //   50,
            //   //   (index) => Container(
            //   //     child: Text('$index'),
            //   //     height: 50,
            //   //     color: Colors.green,
            //   //   ),
            //   // ),
            // ),
            GridView.builder(
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4,
                childAspectRatio: 1,
              ),
              scrollDirection: Axis.vertical,
              itemCount: 20,
              itemBuilder: (context, index) => Container(
                margin: EdgeInsets.all(5),
                // height: 50,
                color: Colors.green,
                child: GestureDetector(
                  onTap: () {
                    debugPrint('$index');
                    if (index == 5) {
                      Navigator.pushNamed(
                        context,
                        "/notFound",
                        arguments: {
                          "aa": ["11", "22"],
                          "index": index,
                          "login": false,
                        },
                      );
                      return;
                    }
                    Navigator.pushNamed(
                      context,
                      "/detail",
                      arguments: {
                        "aa": ["11", "22"],
                        "index": index,
                        "login": false,
                      },
                    );
                    // Navigator.push(
                    //   context,
                    //   MaterialPageRoute(
                    //     builder: (context) =>
                    //         UseStatePageDetail(title: "详情$index"),
                    //   ),
                    // );
                  },
                  child: Text('$index'),
                ),
              ),
              // crossAxisCount: 3,
              // children: List.generate(
              //   50,
              //   (index) => Container(
              //     margin: EdgeInsets.all(5),
              //     // height: 50,
              //     color: Colors.green,
              //     child: Text('$index'),
              //   ),
              // ),
            ),
      ),
    );
  }
}

class UseStatePageDetail extends StatefulWidget {
  final String? title;
  const UseStatePageDetail({super.key, this.title});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _UseStatePageDetail();
  }
}

class _UseStatePageDetail extends State<UseStatePageDetail> {
  @override
  void initState() {
    // TODO: implement initState
    Future.microtask(() {
      var route = ModalRoute.of(context);
      // print(route!.settings.name);
      if (route != null && route.settings.arguments != null) {
        var arguments = route.settings.arguments;
        // int index = arguments[0];
        debugPrint('arguments $arguments');
      }
    });
    super.initState();
    debugPrint('initState');
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(title: Text('Detail')),
      body: Container(
        child: TextButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: Text("返回${widget.title}"),
        ),
      ),
    );
  }
}

class UseStatePageLogin extends StatefulWidget {
  final String? title;
  const UseStatePageLogin({super.key, this.title});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _UseStatePageLogin();
  }
}

class _UseStatePageLogin extends State<UseStatePageLogin> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    debugPrint('initState');
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Container(
        child: TextButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: Text("返回"),
        ),
      ),
    );
  }
}

class UseStatePageNotFound extends StatefulWidget {
  final String? title;
  const UseStatePageNotFound({super.key, this.title});

  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    debugPrint('createState');
    return _UseStatePageNotFound();
  }
}

class _UseStatePageNotFound extends State<UseStatePageNotFound> {
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    debugPrint('initState');
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(title: Text('NotFound')),
      body: Container(
        child: TextButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: Text("返回"),
        ),
      ),
    );
  }
}

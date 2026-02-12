import 'package:flutter/material.dart';
import 'package:flutter/widget_previews.dart';

void main(List<String> args) {
  runApp(UseStatePage());
}

class UseStatePage extends StatefulWidget {
  // @Preview(size: Size(300, 800))
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
              scrollDirection: Axis.horizontal,
              itemCount: 50,
              itemBuilder: (context, index) => Container(
                margin: EdgeInsets.all(5),
                // height: 50,
                color: Colors.green,
                child: Text('$index'),
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

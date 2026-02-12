import 'package:flutter/material.dart';

void main(List<String> args) {
  runApp(
    MaterialApp(
      title: 'Hello My Flutter3',
      // theme: ThemeData(scaffoldBackgroundColor: Colors.blue),
      home: Scaffold(
        appBar: AppBar(
          title: Text('Hello My Flutter2'),
          actions: [IconButton(onPressed: () {}, icon: Icon(Icons.settings))],
        ),
        body: Center(child: Text('Hello Flutter')),
        bottomNavigationBar: SizedBox(
          height: 50,
          child: Center(child: Text('BottomNavigationBar')),
        ),
        // bottomNavigationBar: Container(
        //   // SizedBox(width: 4, child: Text('...')),
        //   height: 50,
        //   child: Center(child: Text('BottomNavigationBar')),
        // ),
        // bottomNavigationBar: BottomNavigationBar(
        //   items: [
        //     BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
        //     BottomNavigationBarItem(
        //       icon: Icon(Icons.business),
        //       label: 'Business',
        //     ),
        //     BottomNavigationBarItem(icon: Icon(Icons.school), label: 'School'),
        //   ],
        // ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {},
          child: Icon(Icons.access_alarm_outlined),
        ),
      ),
    ),
  );
}

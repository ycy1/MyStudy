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

        floatingActionButton: FloatingActionButton(
          onPressed: () {},
          child: Icon(Icons.access_alarm_outlined),
        ),
      ),
    ),
  );
}

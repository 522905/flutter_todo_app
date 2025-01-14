import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hive_flutter/adapters.dart';
import 'package:practice_1/todo-app/home_page.dart';

void main() async {

  await Hive.initFlutter();

  var box = await Hive.openBox('mybox');

  runApp(  MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return  MaterialApp(
      debugShowCheckedModeBanner: false,
      home:  const HomePage(),
      theme: ThemeData(
    primarySwatch: Colors.yellow,
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: Colors.yellow,
    ),
),
    );
  }
}

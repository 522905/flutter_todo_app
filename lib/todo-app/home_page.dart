import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import 'package:practice_1/Util/toDo_tile.dart';
import 'package:practice_1/data/database.dart';

import '../Util/dialog_box.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  
  final _myBox = Hive.box('mybox');
  
  ToDoDataBase db = ToDoDataBase();

  @override
  void initState() {
    if(_myBox.get('TODOLIST') == null)
    {
      db.createInitialData();
    }
    else
    {
      db.loadData();
    }
    super.initState();
  }

  final taskController = TextEditingController();

  void checkBoxChanged(bool? value, int index)
  {
    setState(() {
      db.toDoList[index]['isDone'] = !db.toDoList[index]['isDone'];
    });
    db.updateDataBase();
  }

  void createNewTask()
  {
    showDialog(
        context: context,
        builder: (context){
          return DialogBox(
            taskController: taskController,
            savedTask: (){
              setState((){
                db.toDoList.add({
                  'title': taskController.text,
                  'isDone': false
                });
                Navigator.pop(context);
                taskController.clear();
              });
              db.updateDataBase();
            },
            cancelTask: (){
              Navigator.pop(context);
              taskController.clear();
            },
          );
        });
  }
  void deleteTask(int index)
  {
    setState((){
      db.toDoList.removeAt(index);
    });
    db.updateDataBase();
  }


  @override
  Widget build(BuildContext context) {
    return  Scaffold(
      backgroundColor: Colors.yellow[200],
      appBar: AppBar(
        backgroundColor: Colors.yellow,
        foregroundColor: Colors.white,
        title: const Center(child: Text("TO-DO")),
        elevation: 0,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: (){
          createNewTask();
        },
        child: const Icon(Icons.add),
      ),
      body: ListView.builder(
        itemCount: db.toDoList.length,
        itemBuilder: (context,index){
          return ToDoTile(
            taskName: db.toDoList[index]['title'],
            taskCompleted: db.toDoList[index]['isDone'],
            onChanged: (value)
            {
              checkBoxChanged(value, index);
            },
            deleteFunction: (context) => deleteTask(index),
          );
        },
      )
    );
  }
}

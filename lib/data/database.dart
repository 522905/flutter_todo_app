import 'package:hive/hive.dart';

class ToDoDataBase {

  List toDoList =[];

  final _myBox = Hive.box('mybox');

  void createInitialData(){
    toDoList = [
      {
        'title': 'Task 1',
        'isDone': false
      },
      {
        'title': 'Task 2',
        'isDone': false
      },
    ];
  }

  void loadData() {
    toDoList = _myBox.get('TODOLIST');
  }

  void updateDataBase() {
    _myBox.put('TODOLIST', toDoList);
  }
}
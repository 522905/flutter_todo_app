import 'dart:ui';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';

class ToDoTile extends StatelessWidget {
  final String taskName;
  final bool taskCompleted;
  Function(bool?)? onChanged;
  Function(BuildContext)? deleteFunction;
  ToDoTile ({
      super.key,
       required this.taskName,
       required this.taskCompleted,
       required this.onChanged,
      required this.deleteFunction
    });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding:  EdgeInsets.all(25.0),
      child: Slidable(
        endActionPane: ActionPane(
          motion: ScrollMotion(),
          children: [
            SlidableAction(
                onPressed: deleteFunction,
              icon: Icons.delete,
              backgroundColor: Colors.red,
              borderRadius: BorderRadius.circular(12),
            )
          ],
        ),
        child: Container(
          padding: const EdgeInsets.all(20.0),
          decoration: const BoxDecoration(
              color: Colors.yellow,
            borderRadius: BorderRadius.all(Radius.circular(12)),
          ),
          child:  Row(
            children: [
              Checkbox(
                value: taskCompleted,
                onChanged: onChanged,
                activeColor: Colors.black,
              ),
              const SizedBox(width: 10,),
              Text(taskName,
                style: TextStyle(
                    fontSize: 20,
                    decoration:
                    taskCompleted
                    ? TextDecoration.lineThrough
                    : TextDecoration.none
                ),),
            ],
          ),
        ),
      ),
    );
  }
}

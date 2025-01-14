import 'package:flutter/material.dart';
import 'my_button.dart';

class DialogBox extends StatelessWidget {
  final taskController;
  VoidCallback savedTask;
  VoidCallback cancelTask;
   DialogBox({
     super.key,
     required this.taskController,
     required this.savedTask,
     required this.cancelTask,
  });


  @override
  Widget build(BuildContext context) {
    return Theme(
      data: Theme.of(context).copyWith(
        dialogBackgroundColor: Colors.yellow,
      ),
      child: AlertDialog(
        content: Padding(
          padding: const EdgeInsets.all(15.0),
          child: Container(
            height: 150,
            child: Column(
              children: [
                 TextField(
                  controller: taskController ,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(
                    ),
                    hintText: "Add new Task",

                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    MyButton(
                      text: 'Add',
                      onPressed: () {
                        savedTask();
                      },
                    ),
                    MyButton(
                      text: 'Cancel',
                      onPressed: () {
                        cancelTask();
                      },
                    )
                  ],
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
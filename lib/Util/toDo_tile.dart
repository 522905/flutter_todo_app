import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class ToDoTile extends StatefulWidget {
  final String taskName;
  final bool taskCompleted;
  final Function(bool?)? onChanged;
  final Function(BuildContext)? deleteFunction;

  const ToDoTile({
    super.key,
    required this.taskName,
    required this.taskCompleted,
    required this.onChanged,
    required this.deleteFunction,
  });

  @override
  State<ToDoTile> createState() => _ToDoTileState();
}

class _ToDoTileState extends State<ToDoTile> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 200),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: Slidable(
          key: ValueKey(widget.taskName),
          endActionPane: ActionPane(
            motion: const StretchMotion(),
            dismissible: DismissiblePane(
              onDismissed: () {
                if (widget.deleteFunction != null) {
                  widget.deleteFunction!(context);
                }
              },
            ),
            children: [
              SlidableAction(
                onPressed: widget.deleteFunction,
                backgroundColor: const Color(0xFFFF6584),
                foregroundColor: Colors.white,
                icon: FontAwesomeIcons.trash,
                label: 'Delete',
                borderRadius: BorderRadius.circular(16),
              ),
            ],
          ),
          child: GestureDetector(
            onTapDown: (_) => _controller.forward(),
            onTapUp: (_) => _controller.reverse(),
            onTapCancel: () => _controller.reverse(),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: widget.taskCompleted
                      ? [
                          const Color(0xFFE8F5E9).withOpacity(0.7),
                          const Color(0xFFC8E6C9).withOpacity(0.7),
                        ]
                      : [
                          Colors.white,
                          Colors.white.withOpacity(0.95),
                        ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(
                    color: widget.taskCompleted
                        ? const Color(0xFF00D4AA).withOpacity(0.2)
                        : const Color(0xFF6C63FF).withOpacity(0.1),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
                border: Border.all(
                  color: widget.taskCompleted
                      ? const Color(0xFF00D4AA).withOpacity(0.3)
                      : const Color(0xFF6C63FF).withOpacity(0.2),
                  width: 1.5,
                ),
              ),
              child: Row(
                children: [
                  // Custom animated checkbox
                  GestureDetector(
                    onTap: () {
                      if (widget.onChanged != null) {
                        widget.onChanged!(!widget.taskCompleted);
                      }
                    },
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 300),
                      width: 28,
                      height: 28,
                      decoration: BoxDecoration(
                        gradient: widget.taskCompleted
                            ? const LinearGradient(
                                colors: [Color(0xFF00D4AA), Color(0xFF00B894)],
                              )
                            : LinearGradient(
                                colors: [
                                  Colors.white,
                                  const Color(0xFF6C63FF).withOpacity(0.1),
                                ],
                              ),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: widget.taskCompleted
                              ? const Color(0xFF00D4AA)
                              : const Color(0xFF6C63FF).withOpacity(0.5),
                          width: 2,
                        ),
                      ),
                      child: widget.taskCompleted
                          ? const Icon(
                              Icons.check_rounded,
                              color: Colors.white,
                              size: 20,
                            )
                          : null,
                    ),
                  ),
                  const SizedBox(width: 16),
                  // Task text
                  Expanded(
                    child: Text(
                      widget.taskName,
                      style: GoogleFonts.poppins(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                        color: widget.taskCompleted
                            ? const Color(0xFF4F5D75).withOpacity(0.6)
                            : const Color(0xFF2D3142),
                        decoration: widget.taskCompleted
                            ? TextDecoration.lineThrough
                            : TextDecoration.none,
                        decorationColor: const Color(0xFF00D4AA),
                        decorationThickness: 2,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Status icon
                  AnimatedOpacity(
                    duration: const Duration(milliseconds: 300),
                    opacity: widget.taskCompleted ? 1.0 : 0.3,
                    child: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: widget.taskCompleted
                            ? const Color(0xFF00D4AA).withOpacity(0.1)
                            : const Color(0xFF6C63FF).withOpacity(0.05),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: FaIcon(
                        widget.taskCompleted
                            ? FontAwesomeIcons.circleCheck
                            : FontAwesomeIcons.circle,
                        color: widget.taskCompleted
                            ? const Color(0xFF00D4AA)
                            : const Color(0xFF6C63FF),
                        size: 16,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Rooted Device Access Check')),
        body: Center(
          child: RootCheckButton(),
        ),
      ),
    );
  }
}

class RootCheckButton extends StatelessWidget {
  static const platform = MethodChannel('com.example/root_check');

  Future<void> _checkRoot() async {
    try {
      final bool isRooted = await platform.invokeMethod('isRooted');
      if (isRooted) {
        print('Device is rooted');
      } else {
        print('Device is not rooted');
      }
    } on PlatformException catch (e) {
      print("Failed to check root status: '${e.message}'.");
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: _checkRoot,
      child: Text('Check if Device is Rooted'),
    );
  }
}

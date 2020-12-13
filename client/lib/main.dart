import 'package:flutter/material.dart';
import './createUser.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import './client.dart';
import './login.dart';

void main() {
  // WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
  print("hello");
}

//carefull alignment is between 1 and -1

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
      // client: clientFor(uri: "http://localhost:5000/graphql"),
      // client: clientFor(uri: "http://10.0.2.2:5000/graphql"),
      client: clientFor(uri: getUri()),
      child: MaterialApp(
            title: 'What is this Flower',
            theme: ThemeData(
              primarySwatch: Colors.green,
            ),
            home: Scaffold(
              appBar: AppBar(title: Text('Login')),
              body: Column(
                children: [
                  Align (
                    alignment: Alignment(0.0, -0.75),
                    child: CreateLogin(),
                  ),
                  Align (
                    alignment: Alignment(-1.0, 1),
                    child: ButtonCreateUser(),
                  )
                ]
              ),
              backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
              // body: Center(child: RawWords()),
            ),
          )
    );
    
    
    
    
  }
}

// class RawWords extends StatefulWidget {
//   @override
//   RawWordState createState() => RawWordState();
// }

// class RawWordState extends State<RawWords>
// {
//   final _username = GlobalKey<FormState>();
//   @override
//   Widget build(BuildContext context) {
//     // final word = "on est laaaa";
//     // return Text(word);
//     return Form(
//       key: _username,
//       child: Column(
//         children: <Widget> [
//           TextFormField(
//             decoration: const InputDecoration(
//               hintText: 'username',
//             ),
//             validator: (value) {
//               if (value.isEmpty) {
//                 return 'Please enter your username';
//               }
//               return null;
//             },
//           ),
//           TextFormField(
//             decoration: const InputDecoration(
//               hintText: 'password',
//             ),
//             validator: (value) {
//               if (value.isEmpty) {
//                 return 'Please enter your password';
//               }
//               return null;
//             },
//             obscureText: true
//           ),
          
//           Padding(
//             padding: const EdgeInsets.symmetric(vertical: 16.0),
//             child: ElevatedButton(
//               onPressed: () {
//                 // Validate will return true if the form is valid, or false if
//                 // the form is invalid.
//                 if (_username.currentState.validate()) {
//                   // call gql request
//                 }
//               },
//               child: Text('Login'),
//             ),
//           ),
//         ]
//       )
        
//     );

//   }
// }

//Stateless widgets are immutable, meaning that their properties can’t change—all values are final.


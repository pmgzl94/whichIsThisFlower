import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './menu.dart';

//  mutation login(\$username: String!, \$password: String!) {
final String login = """
  mutation Login(\$username: String!, \$password: String!) {
      auth(username: \$username, password: \$password) {
        accessToken
      }
  }
""";

AlertDialog dialog(context, mssg) {
  return AlertDialog(
    title: Text('Error occured'),
    content: SingleChildScrollView(
        child: ListBody(
            children: <Widget>[
                Text(mssg),
            ],
        ),
    ),
    actions: <Widget>[
        TextButton(
            child: Text("Close"),
            onPressed: () {
                Navigator.of(context).pop();
            },
        ),
     ],
  );
}

class CreateLogin extends StatefulWidget
{
    final CameraDescription camera;

    const CreateLogin({
        Key key,
        @required this.camera,
    }) : super(key: key);

    @override
    CreateLoginState createState() => CreateLoginState();
}

class CreateLoginState extends State<CreateLogin>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked()
    {
      this.state = true;
    }

    final mc1 = TextEditingController();
    final mc2 = TextEditingController();

    @override
    void dispose()
    {
    // Clean up the controller when the widget is disposed.
      mc1.dispose();
      mc2.dispose();
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return Form(
            key: _id,
            child: Column(
              children: <Widget> [
                Padding(
                  padding: EdgeInsets.only(left: 25.0, right: 25.0, top: 25.0),
                  child: TextFormField(
                    decoration: const InputDecoration(
                        hintText: 'username',
                    ),
                    validator: (value) {
                        if (value.isEmpty) {
                          return 'Please enter your username';
                        }
                        return null;
                    },
                    controller: mc1,
                  ),
                ),
                Padding(
                  padding: EdgeInsets.only(left: 25.0, right: 25.0, top: 25.0),
                  child: TextFormField(
                    decoration: const InputDecoration(
                        hintText: 'password',
                    ),
                    validator: (value) {
                        if (value.isEmpty) {
                          return 'Please enter your password';
                        }
                        return null;
                    },
                    controller: mc2,
                    obscureText: true,
                  ),
                ),
                Mutation(
                  options: MutationOptions(
                    documentNode: gql(login),
                    update: (Cache cache, QueryResult result) {
                      return cache;
                    },
                    onError: (result) {
                      print("error");
                      print(result);
                    },
                    onCompleted: (dynamic resultData) {
                      print("on completed");
                      print(resultData.data);
                      if (resultData != null) {
                        print(resultData.data["auth"]["accessToken"]);
                        Navigator.push(
                          context,
                          // MaterialPageRoute(builder: (context) => CreateMenu(token: resultData.data["auth"]["accessToken"],
                          MaterialPageRoute(builder: (context) => Menu(token: resultData.data["auth"]["accessToken"],
                                                     camera: widget.camera
                          )),
                        );
                      } else {
                        print("User doesn't exist");
                        showDialog<AlertDialog>(
                          context: context,
                          builder: (BuildContext context) {
                            return dialog(context, "User doesn't exist");
                        });
                      }
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                               primary: Color.fromRGBO(0, 102, 0, 0.6),
                          ),
                          onPressed: () {
                            runMutation({"username": mc1.text, "password": mc2.text});
                          },
                          child: Text('Login'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}

class ButtonCreateLogin extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
      return ElevatedButton(
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => CreateLogin()),
                );
              },
              child: Text('Login'),
            );
  }
}
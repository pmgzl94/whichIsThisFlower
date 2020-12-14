import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

final String takePic = """
  mutation logout(\$token: String!) {
      logout(token: \$token) {
          ok {
            ... on IsOk {
                ok
              }
          }
      }
  }
""";

class CreateTakePictureButton extends StatefulWidget
{
  final String token;
  CreateTakePictureButton({Key key, @required this.token}) : super(key: key);

  @override
  CreateTakePictureButtonState createState() => CreateTakePictureButtonState();
}

class CreateTakePictureButtonState extends State<CreateTakePictureButton>
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
    void dispose() {
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
               Mutation(
                  options: MutationOptions(
                    documentNode: gql(takePic),
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
                      print("takePICTURE");
                      Navigator.pop(context);
                    }
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: ElevatedButton(
                          onPressed: () async {
                            print("GET TOKENNNNNNN");
                            print(widget.token);
                            print("GET ENDED");
                            runMutation({"token": widget.token});
                          },
                          child: Text('Take Picture'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}

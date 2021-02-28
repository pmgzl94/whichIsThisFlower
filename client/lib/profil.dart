import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:camera/camera.dart';
import './seePictures.dart';
import './takePicture.dart';
import './createUser.dart';
import './login.dart';


final String logout = """
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

class CreateProfil extends StatefulWidget
{
    final String token;
    final String username;

    CreateProfil({Key key,
                  @required this.token,
                  @required this.username,
             }) : super(key: key);

    @override
    CreateProfilState createState() => CreateProfilState();
}

class CreateProfilState extends State<CreateProfil>
{
    bool _status = true;


    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
                title: Text('PROFILE'),
                centerTitle: true,
                automaticallyImplyLeading: false,
        ),
        body: new ListView(
          children: <Widget>[
            Column(
              children: [
                new Container(
                  height: 250.0,
                  color: Colors.white,
                  // color: Color.fromRGBO(230, 255, 255, 0.6),
                  child: new Column(
                    children: <Widget>[
                      Padding(
                        padding: EdgeInsets.only(top: 50.0),
                        child: new Stack(fit: StackFit.loose, children: <Widget>[
                          new Row(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: <Widget>[
                              new Container(
                                  width: 140.0,
                                  height: 140.0,
                                  decoration: new BoxDecoration(
                                    shape: BoxShape.circle,
                                    image: new DecorationImage(
                                      image: new ExactAssetImage(
                                          './assets/images/profile.png'),
                                      fit: BoxFit.cover,
                                    ),
                                  )),
                            ],
                          ),
                        ]),
                      )
                    ]
                  )
                ),
                new Container(
                  color: Color(0xffFFFFFF),
                  child: Padding(
                    padding: EdgeInsets.only(bottom: 25.0),
                    child: new Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: <Widget>[
                        Padding(
                            padding: EdgeInsets.only(
                                left: 25.0, right: 25.0, top: 25.0),
                            child: new Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              mainAxisSize: MainAxisSize.max,
                              children: <Widget>[
                                new Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  mainAxisSize: MainAxisSize.min,
                                  children: <Widget>[
                                    new Text(
                                      'Personal Information',
                                      style: TextStyle(
                                          fontSize: 18.0,
                                          fontWeight: FontWeight.bold),
                                    ),
                                  ],
                                ),
                              ],
                            )),
                        Padding(
                            padding: EdgeInsets.only(
                                left: 25.0, right: 25.0, top: 25.0),
                            child: new Row(
                              mainAxisSize: MainAxisSize.max,
                              children: <Widget>[
                                new Column(
                                  mainAxisAlignment: MainAxisAlignment.start,
                                  mainAxisSize: MainAxisSize.min,
                                  children: <Widget>[
                                    new Text(
                                      'Username',
                                      style: TextStyle(
                                          fontSize: 16.0,
                                          fontWeight: FontWeight.bold),
                                    ),
                                  ],
                                ),
                              ],
                            )),
                        Padding(
                            padding: EdgeInsets.only(
                                left: 25.0, right: 25.0, top: 10.0),
                            child: new Row(
                              mainAxisSize: MainAxisSize.max,
                              children: <Widget>[
                                new Flexible(
                                  child: new Text(widget.username),
                                ),
                              ],
                            )),

                        !_status ? _getActionButtons() : new Container(),
                      ],
                    ),
                  ),
                )
              ]
            ),
            Align (
              alignment: Alignment(0.0, -0.75),
              child: CreateLogoutButton(token: widget.token),
            ),
          ]
        ),
        backgroundColor: Colors.white,
        // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
      );
    }


    Widget _getActionButtons() {
      return Padding(
        padding: EdgeInsets.only(left: 25.0, right: 25.0, top: 45.0),
        child: new Row(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Expanded(
              child: Padding(
                padding: EdgeInsets.only(right: 10.0),
                child: Container(
                    child: new RaisedButton(
                  child: new Text("Save"),
                  textColor: Colors.white,
                  color: Colors.green,
                  onPressed: () {
                    setState(() {
                      _status = true;
                      FocusScope.of(context).requestFocus(new FocusNode());
                    });
                  },
                  shape: new RoundedRectangleBorder(
                      borderRadius: new BorderRadius.circular(20.0)),
                )),
              ),
              flex: 2,
            ),
            Expanded(
              child: Padding(
                padding: EdgeInsets.only(left: 10.0),
                child: Container(
                    child: new RaisedButton(
                  child: new Text("Cancel"),
                  textColor: Colors.white,
                  color: Colors.red,
                  onPressed: () {
                    setState(() {
                      _status = true;
                      FocusScope.of(context).requestFocus(new FocusNode());
                    });
                  },
                  shape: new RoundedRectangleBorder(
                      borderRadius: new BorderRadius.circular(20.0)),
                )),
              ),
              flex: 2,
            ),
          ],
        ),
      );
    }

    Widget _getEditIcon()
    {
        return new GestureDetector(
          child: new CircleAvatar(
            // backgroundColor: Colors.red,
            radius: 14.0,
            child: new Icon(
              Icons.edit,
              color: Colors.white,
              size: 16.0,
            ),
          ),
          onTap: () {
            setState(() {
              _status = false;
            });
          },
        );
    }
}

class CreateLogoutButton extends StatefulWidget
{
    final String token;
    CreateLogoutButton({Key key, @required this.token}) : super(key: key);

    @override
    CreateLogoutButtonState createState() => CreateLogoutButtonState();
}

class CreateLogoutButtonState extends State<CreateLogoutButton>
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
                    documentNode: gql(logout),
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
                      print("LOGOUT");
                      Navigator.maybePop(context);
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
                          child: Text('Logout'),
                        )
                    );
                  }
                )
              ]
            )
          );
    }
}

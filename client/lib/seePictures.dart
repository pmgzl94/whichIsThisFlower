import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

final String seePic = """
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

AlertDialog a(context, mssg) {return AlertDialog(
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

class CreateSeePictureButton extends StatefulWidget
{
  final String token;
  CreateSeePictureButton({Key key, @required this.token}) : super(key: key);
  
  @override
  CreateSeePictureButtonState createState() => CreateSeePictureButtonState();
}

class CreateSeePictureButtonState extends State<CreateSeePictureButton>
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
		    documentNode: gql(seePic),
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
		      print("SEE PICTURES");
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
			  child: Text('Pictures taken'),
			)
		    );
		  }
		)
	      ]
	    )
	  );
    }
}

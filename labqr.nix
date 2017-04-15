{ pythonPackages }:
with pythonPackages;

buildPythonPackage {
  name = "labqr-0.1";
  namePrefix = "";
  src = ./.;
  propagatedBuildInputs = [
    docopt
    reportlab
    shortuuid
  ];
  doCheck = false;
  dontStrip = true;
}

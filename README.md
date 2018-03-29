DANS Maven Parents
==================
Parents for DANS Maven based projects.


SYNOPSIS
--------

    <parent>
       <groupId>nl.knaw.dans.shared</groupId>
       <artifactId>dans-java-project</artifactId>
       <version>2.0.0</version>
    </parent>

or:

    <parent>
       <groupId>nl.knaw.dans.shared</groupId>
       <artifactId>dans-scala-project</artifactId>
       <version>2.0.0</version>
    </parent>


DESCRIPTION
-----------
This module defines several Maven parent projects for use in DANS Maven based projects.

### Goals
This is done to achieve the following goals.

* To define default versions and scopes for commonly used dependencies. This is done by declaring
  managed dependencies in the base modules. The inheriting project then only needs to declare the
  dependency using the `groupId` and `artifactId` to automatically use the defaults, while it can
  still override those, if necessary.
* To define default versions and configurations for commonly used plug-ins. This is doen by declaring
  managed plug-ins, which the same as managed dependencies. This saves even more space in the inheriting
  project, as plug-in configurations can be rather long.
* To declare a few dependencies and plug-ins that are (almost) always used in DANS projects. However, this
  is only done in the sub-modules lowest in the hierarchy, so if you really do not need those dependencies
  you can inherit from a parent higher in the tree.

### Main features


### Design
A of writing this, Maven is unfortunately still rather low in composability. This means that, to split up a
POM you do not have a lot of options. If you have to use the managed dependencies you are basically stuck with
splitting up over a single-inheritance hierarchy, so that is what we have done here. This hierarchy is subdivided
as follows:

                                    dans-mvn-base
                                         |
                                dans-mvn-plugin-defaults
                                         |
                                 dans-mvn-lib-defaults
                                         |
                                  -------------------
                                  |                 |
                            dans-java-parent     dans-scala-parent


POM                        | Description
---------------------------|-------------------------------------------------------------
`dans-mvn-base`            | Only basic facilities needed by all projects.
`dans-mvn-plugin-defaults` | Only managed plug-in configurations.
`dans-mvn-lib-defaults`    | Only managed dependency configurations.
`dans-java-parent`         | The basic dependencies and plug-ins needed for any DANS Java project.
`dans-scala-parent`        | The basic dependencies and plug-ins needed for any DANS Scala project.

Note that this means that only the latter two projects declare any dependencies or plug-ins actually inherited by your
project. (Actually, `dans-mvn-base` also does, but it is one plug-in dependency you can easily ignore.)

INSTALLATION AND CONFIGURATION
------------------------------
To use these parents you need to add two thing to you POM file:

* The parent project you want to inherit from. In most cases this should be `dans-scala-project` or
  `dans-java-project`. However, you can also use one of the parents higher up in the inheritance tree.
* The DANS Maven repositories.

This will look like the following. Note that the version in this example may not be the latest available version.

    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
        <parent>
            <groupId>nl.knaw.dans.shared</groupId>
            <artifactId>dans-scala-project</artifactId>
            <version>2.0.0</version>
        </parent>
        <!-- ... -->
        <repositories>
            <repository>
                <id>DANS</id>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <url>http://maven.dans.knaw.nl/</url>
            </repository>
        </repositories>
        <pluginRepositories>
            <pluginRepository>
                <id>DANS</id>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <url>http://maven.dans.knaw.nl/</url>
            </pluginRepository>
        </pluginRepositories>
        <!-- ... -->
    </project>


BUILDING FROM SOURCE
--------------------
Prerequisites:

* Java 8 or higher
* Maven 3.3.3 or higher

Steps:

    git clone https://github.com/DANS-KNAW/dans-mvn-parent.git
    cd dans-mvn-parent
    mvn install

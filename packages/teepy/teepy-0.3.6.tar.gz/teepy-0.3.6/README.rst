=====
TEEPy
=====

TEEPy stands for Tech Engineering Exam in Python. TEEPy's aim is to make an
easy-to-use framework to create clean and professional-looking paper-based
assessments (e.g., quiz, exam, etc.) with a focus on STEM (Science, Technology,
Engineering, and Math) related topics. There are two intended end-users of
TEEPy, question creators (QCs), and assessment creators (ACs). QCs create
individual questions or problems that will be used in a particular assessment
that an AC will use to create the overall assessment. TEEPy accomplishes these
goals by generating all question and assessment content as HTML and then
rendering the HTML to create PDFs (using a combination of cefpython_ and
pyppeteer_). There is also some `Beautiful Soup`_ thrown in there as well. TEEPy
supports the use of LaTex_ (via MathJax_) as well as the use of units (using the
package pint_). TEEPy is capable of randomizing question placement and answer
choices to questions.

Installation
============

Installation is a simple matter of

.. code-block:: bash

    $ pip install teepy

and then enjoy!

Roles
=====

There are two roles that an end-user of TEEPy can assume, question creator (QC)
or assessment creator (AC). QCs deal solely with individual questions or problem
creation. ACs deal with the assessment as a whole. ACs take one or more
questions created by QCs and make an assessment out of the selected questions.

Question Creator (QC)
---------------------

The goal of a QC is to create individual questions that are self-contained. The
content and calculations in the individual question file will not interact with
content and calculations performed in another question file. Each question file
must contain two function definitions, a :code:`PROBLEM()` function and a
:code:`CHOICES()` function. Each of these functions takes one argument, an index
value variable. The index value is used to create different versions of a
particular question. The :code:`PROBLEM()` function uses the function's
docstring to define the problem statement and should return a dictionary
containing at least a  key of :code:`answer`. If the question has no answer
(e.g., in the case of an open-ended question), a :code:`None` may be returned
from the :code:`PROBLEM()` function. An example of an open-ended question is
shown below.

.. code-block:: python

    # An open-ended question
    def PROBLEM(ind):
        '''What is the meaning of life?'''

        return None

Even if there are no different versions of the question, the :code:`PROBLEM()`
should be a function of the index variable :code:`ind`.

In the event a question does have a correct answer (or answers), the value of
the key :code:`answer` should be a single value or a list of values (in the case
of a multiple answer problem). An example of a single answer question is shown
below.

.. code-block:: python

    # A single answer question
    def PROBLEM(ind):
        '''What color is the sky?'''

        answer = 'Blue'

        return {'answer': answer}

An example of a multiple-answer question is shown below.

.. code-block:: python

    # A multiple-answer question
    def PROBLEM(ind):
        '''How many licks does it take to get to the center of a Tootsie Pop?'''

        answer = [3, 'The world may never know.']

        return {'answer': answer}

The return value of :code:`PROBLEM()` may also contain a key of :code:`given`.
The value of the key :code:`given` should be a dictionary that includes any
variables used in the question statement. An example of using a given variable
is shown below.

.. code-block:: python

    # A question with a given variable
    def PROBLEM(ind):
        '''A {object} is an example of what?'''

        obj = ['dog', 'carrot', 'diamond']

        answers = ['Animal', 'Vegatable', 'Mineral']

        given = {'object': obj[ind]}

        return {'answer': answers[ind], 'given': given}

It should be noted in the example above that three different versions of the
questions may be created by simply changing the :code:`ind` variable to a value
of zero, one, or two. Units may also be used in the :code:`PROBLEM()` function.
An example of utilizing units is shown below.

.. code-block:: python

    import teepy

    def PROBLEM(ind):
        '''If points A, B, and C lie along a straight line in that order,
    and the distance between point A and B is $ {L1} $, and the distance
    between point B and C is $ {L2} $, what is the distance between point
    A and C?'''

        L1s = [1, 2, 3]
        L2s = [4, 5, 6]

        L1 = teepy.define_unit(L1s[ind], 'ft')
        L2 = teepy.define_unit(L2s[ind], 'cm')

        L = L1 + L2

        answer = L.to('m')
        given = {'L1': L1,
                 'L2': L2}

        return {'answer': answer, 'given': given}

There are a few things to note about the example above. If a given variable has
units, the rendered version of the variable (i.e., what is in the problem
statement) needs to be enclosed in dollar signs. The units of a given variable
get converted into LaTeX. LaTeX code that is not enclosed in dollar signs will
not be rendered as LaTeX. The TEEPy function :code:`define_unit` may be used to
assign units to a variable. This function is :code:`pint`'s :code:`Q_` function
(please refer to :code:`pint`'s documentation on how to use it). Once units have
been assigned to a variable, calculations performed with those variables will
automatically perform the necessary conversions when dealing with different
types of units.

The :code:`CHOICES()` function must return a :code:`None` value, or a dictionary
containing the key :code:`choices`. No multiple-choice choices will be displayed
if :code:`CHOICES()` returns a :code:`None` value. An open-ended question is
typically when this is needed. Below is an example of a :code:`CHOICES()`
function that returns a :code:`None` value.

.. code-block:: python

    def CHOICES(ind):

        return None

If multiple-choice answers are provided, the :code:`CHOICES()` function should
return a dictionary containing the key :code:`choices`. The value of this key
should be a list containing the correct answer and wrong answers. In other
words, it should include everything that is to be listed as answer choices in
the question. An example of using the :code:`choices` key-value pair is shown
below.

.. code-block:: python

    import teepy

    def CHOICES(ind):
        choices = teepy.get_answers(PROBLEM(ind))

        choices.extend(['Red',
                        'Green',
                        'Yellow',
                        'Orange'])

        random.shuffle(choices)

        return {'choices': choices}

The example above also illustrates the use of a TEEPy function called
:code:`get_answers()`. The function takes one argument of a :code:`PROBLEMS()`
function with the particular index value that is to used. The function always
returns a list even if the answer to the problem is a single value answer. The
example above also demonstrates the use of Python's built-in module
:code:`random`. :code:`random` has many useful methods but the one here shuffles
a list. The list of choices does not have to be rearranged. An example of not
mixing the list of options is shown below.

.. code-block:: python

    import teepy

    def CHOICES(ind):
        choices = [1, 2]
        choices.extend(teepy.get_answers(PROBLEM(ind)))

        return {'choices': choices}

There are a couple of things worth mentioning about the :code:`CHOICES()`
function when an answer has units. When an answer has units, TEEPy has the
function :code:`generate_choices()` available to generate randomized choices.
The function takes three arguments; the number of choices, the correct answer,
and the step size between choices. The :code:`CHOICES()` function must also have
a key :code:`choice_format` in the dictionary it returns. The value of this key
is the desired format type of the answer choices. An example of using the
:code:`generate_choices()` function and the :code:`choice_format` key is shown
below.

.. code-block:: python

    import teepy

    def CHOICES(ind):
        N = 10
        choice_format = '{:0.3f}'
        step = random.uniform(0.01, 0.05)
        ans = teepy.get_answers(PROBLEM(ind))

        choices = teepy.generate_choices(N, ans, step)

        return {'choices': choices, 'choice_format': choice_format}

All of the examples seen above may be found in the examples directory.

Assessment Creator (AC)
-----------------------

An assessment creator (AC) is an individual that takes questions created by QCs
and arranges them to form an assessment (e.g., quiz, exam, etc.). The AC will
design the assessment layout and set the question point values. To do so, an AC
will initialize a :code:`teepy.begin()` class. This class will be the handle for
structuring the assessment content. When initializing the class, two arguments
are typically used; :code:`n_forms` and :code:`n_inds`. :code:`n_forms` sets the
number of randomized forms to generate. This value is typically the number of
students taking the assessment. The :code:`n_inds` argument sets the number of
versions each question has. Currently, TEEPy requires the number of versions a
question has to be the same between different questions (i.e., if question A has
three different versions, question B must also have three different versions).
The exception to this rule is if the question's :code:`PROBLEM()` and
:code:`CHOICES()` function do not utilize the :code:`ind` variable (as in the
case of the open-ended question shown previously). An example of initializing
the TEEPy :code:`begin` class is shown below.

.. code-block:: python

    import teepy

    exam = teepy.begin(n_forms = 5, n_inds = 3)

In the example above, the TEEPy :code:`begin` class will generate five
randomized assessments where each question in the assessment has three different
versions. The :code:`begin` class has a method called :code:`HTML` that allows
the addition of arbitrary HTML content to be added to the assessment. An example
of using the :code:`HTML` is shown below.

.. code-block:: python

    exam.HTML('''<div style="text-align: center;">
    <h1>COURSE NAME</h1><br>
    <h2>ASSESMENT NAME</h2><br>
    <h3>DATE</h3><br><br>
    <h3>Form Number: ''' + exam.form_number() + '''</h3><br><br>
    <h4>Printed Name: ________________________________________ </h4>
    </div>''')

In the example above, the method :code:`form_number` is implemented. This method
inserts the randomly generated assessment form number. It is always important to
include this on an assessment. Otherwise, assessment forms may not be
distinguished from each other. Other methods are exposed in the :code:`begin`
class. An example of the :code:`new_page` and :code:`problem` methods are shown
below.

.. code-block:: python

    exam.new_page()

    exam.problem('path/to/question/file', 5)

The :code:`new_page` method inserts a page break at its placement. The
:code:`problem` method is how question files are added to an assessment. The
:code:`problem` method requires two arguments; the path to the question file and
the question's point value if a correct answer is given. The :code:`problem`
method also can accept the keyword arguments of :code:`display_worth`,
:code:`min_height`, and :code:`pts_incorrect`. :code:`display_worth` is a
Boolean that sets whether the question's point value should be displayed or not.
:code:`min_height` sets the minimum height of a question. The value supplied to
:code:`min_height` gets translated into the CSS property of :code:`min-height`
using units of inches (e.g., :code:`min_height = 1.5` means the minimum height
of the problem will be 1.5 inches). This keyword argument is helpful in
questions that require a certain amount of paper space for a student's written
computation. The :code:`pts_incorrect` keyword argument indicates that an
incorrect answer should result in a deduction of points, not just the failure to
earn points. An example of utilizing the various keyword arguments of the method
:code:`problem` is shown below.

.. code-block:: python

    exam.problem('path/to/question/file', 0,
                 display_worth = False,
                 min_height = 2.5,
                 pts_incorrect = -2)

The final method exposed in the TEEPy :code:`begin` class is the :code:`section`
method. This method allows for the grouping of content in the assessment. An
example of its use is shown below.

.. code-block:: python

    concept_section = exam.section(shuffle = True)

    concept_section.problem('path/to/concept/question1', 3)
    concept_section.problem('path/to/concept/quesiton2', 3)

    exam.section(concept_section)

The order of content in a section may be randomized by setting the keyword
argument :code:`shuffle` to :code:`True`. The final step in creating an
assessment is to generate the forms. The assessment forms are generated by
invoking the :code:`generate` method of the TEEPy :code:`begin` class. Utilizing
the :code:`generate` method is shown below.

.. code-block:: python

    exam.generate()

Whenever the :code:`generate` method is invoked, the number of assessment forms
are generated, also well as :code:`n_inds` reference forms (which are assessment
forms with all shuffling disabled and with the correct answers marked), and an
Excel sheet containing assessment key information (i.e., correct answers for a
particular form, etc.). More examples of different functionality of TEEPy can be
found in the examples directory.

.. _`Beautiful Soup`: https://pypi.org/project/beautifulsoup4/
.. _`cefpython`: https://github.com/cztomczak/cefpython
.. _`LaTeX`: https://en.wikipedia.org/wiki/LaTeX
.. _`MathJax`: https://www.mathjax.org/
.. _`pyppeteer`: https://github.com/pyppeteer/pyppeteer
.. _`pint`: https://github.com/hgrecco/pint

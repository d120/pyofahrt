from subprocess import Popen, PIPE
import tempfile, os, shutil
from django.template.loader import get_template
from django.http import HttpResponse

class LaTeX:
    @staticmethod
    def render(context, template_name, assets, app='ofahrtbase'):
        template = get_template(template_name)
        rendered_tpl = template.render(context).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            for asset in assets:
                shutil.copy(os.path.dirname(os.path.realpath(__file__))+'/../'+app+'/assets/'+asset, tempdir)
            process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir,)
            pdflatex_output = process.communicate(rendered_tpl)
            try:
                with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                    pdf = f.read()
            except FileNotFoundError:
                pdf = None
        return (pdf, pdflatex_output)
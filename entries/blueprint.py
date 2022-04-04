from fileinput import filename
from flask import Blueprint,flash,render_template,request,redirect,url_for
from models import Entry, Tag
from helpers import object_list
from entries.form import EntryForm, ImageForm
from app import db,app
from werkzeug.utils import secure_filename
import os

entries = Blueprint('entries',__name__, template_folder='templates')

#dans mon main j'ai spécifié que la racine de mon url serait "entries", donc ici toutes mes routes seront précédés de entries puis "/tags/"...

@entries.route('/results')
def entry_list():
    search = request.args.get('q') 
    if search:
        results = Entry.query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search))
        )
    return render_template("entries/list_entries_search.html", results=results)


@entries.route('/')
def index():
    #query contient la requête sql qui est effectué vers ma bdd et son résultat
    query = Entry.query.order_by(Entry.title.asc())
    return object_list('entries/tag_detail.html', query)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query
    return render_template('entries/tag_index.html', tags=tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    #lors du click pour lister je récupère le slug de mon tag ex : python
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    #ici je récupère les entries reliées au tag récupéré au dessus
    entries = tag.entries.order_by(Entry.title.asc())
    return object_list('entries/tag_detail.html', entries, tag=tag)


@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug==slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)


@entries.route('/create/',methods= ['POST','GET'])
def create():

    form = EntryForm(request.form)
    
    if request.method == 'POST':
        
        form = EntryForm(request.form)
     
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" créé.' %entry.title, 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))  
  
    else:      
        return render_template('entries/create.html', form=form)



@entries.route('/update/<slug>',methods= ['POST','GET'])
def update(slug):

    entry = Entry.query.filter(Entry.slug==slug).first_or_404()
    
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
     
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()

            return redirect(url_for('entries.detail', slug=entry.slug))  
    else: 
        form = EntryForm(obj=entry)     
        return render_template('entries/create.html', entry=entry, form=form)




@entries.route('/delete/<slug>',methods= ['GET'])
def delete(slug):
    entry = Entry.query.filter(Entry.slug==slug).first_or_404()
    flash('Entry "%s" supprimée.' %entry.title, 'success')
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('homepage')) 


@entries.route('/image-upload/',methods= ['POST','GET'])
def image_upload():
    
    if request.method == 'POST':
        form = ImageForm(request.form)
     
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'],
                                    secure_filename(image_file.filename))
            image_file.save(filename)
            flash('Image "%s" enregistrée.' % os.path.basename(filename) , 'success')
            return redirect(url_for('homepage')) 
    else: 
        form = ImageForm()     
        return render_template('entries/image_upload.html', form=form)
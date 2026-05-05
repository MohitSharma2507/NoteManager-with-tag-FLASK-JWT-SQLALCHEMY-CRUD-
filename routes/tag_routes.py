from flask import Blueprint,session,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import db,Note,Tag

tag_bp = Blueprint('tags',__name__)

@tag_bp.route('/add_tag',methods = ['POST'])
@jwt_required()
def add_tag():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({
            'error':'No Data Found'
        }),404
    
    name = data.get('name','').strip()

    if not name:
        return jsonify({
            'error':'Name is required'
        }),400
    
    existing_tag = Tag.query.filter_by(name=name,user_id=int(user_id)).first()
    if  existing_tag:
        return jsonify({
            'error': 'Tag with this name already exists'
        }), 400
    
    tag = Tag(name=name, user_id=int(user_id))
    db.session.add(tag)
    db.session.commit()

    return jsonify({
        'message':'Tag Added',
        'tag':tag.to_dict()
    }),200

@tag_bp.route('/get_tags', methods=['GET'])
@jwt_required()
def get_tags():

    user_id = get_jwt_identity()

    tags = Tag.query.filter_by(user_id=int(user_id)).all()

    return jsonify({
        'tags': [t.to_dict() for t in tags],
        'count': len(tags)
    }), 200

@tag_bp.route('/get_tag/<int:id>', methods=['GET'])
@jwt_required()
def get_tag(id):

    user_id = get_jwt_identity()

    tag = db.session.get(Tag, id)

    if not tag:
        return jsonify({'error':'No Tag Found'}),400
    
    if tag.user_id != int(user_id):
        return jsonify({"error":'Unauthorized'}),403
    
    return jsonify({'tag':tag.to_dict()})

@tag_bp.route('/attach_tag/<int:note_id>', methods=['POST'])
@jwt_required()
def attach_tag(note_id):

    user_id = get_jwt_identity()

    note = db.session.get(Note, note_id)
    print(f"Note----> ${note}")

    if not note:
        return jsonify({'error':'No Note Found'}),404
    
    if note.user_id != int(user_id):
        return jsonify({"error":'Unauthorized'}),403
    
    data = request.get_json()
    if not data or 'tag_id' not in data:
        return jsonify({'error':'Tag id is required'}),400
    
    tag = db.session.get(Tag, data['tag_id'])

    if not tag:
        return jsonify({'error': 'Tag not found'}), 404
    
    if tag.user_id != int(user_id):
        return jsonify({"error":'Unauthorized'}),403
    
    if tag in note.tags:
        return jsonify({'error':'Tag already attached to this note'}),409
    
    note.tags.append(tag)

    db.session.commit()

    return jsonify({
        'message':'Tag attached successfully',
        'note':note.to_dict()
    })

@tag_bp.route('/remove_tag/<int:note_id>', methods=['POST'])
@jwt_required()
def remove_tag(note_id):

    user_id = get_jwt_identity()

    note = db.session.get(Note, note_id)
    print(f"Note----> ${note}")

    if not note:
        return jsonify({'error':'No Note Found'}),404
    
    if note.user_id != int(user_id):
        return jsonify({"error":'Unauthorized'}),403
    
    data = request.get_json()
    if not data or 'tag_id' not in data:
        return jsonify({'error':'Tag id is required'}),400
    
    tag = db.session.get(Tag, data['tag_id'])

    if not tag:
        return jsonify({'error': 'Tag not found'}), 404
    
    if tag.user_id != int(user_id):
        return jsonify({"error":'Unauthorized'}),403
    
    if tag not in note.tags:                
        return jsonify({'error': 'Tag not attached to this note'}), 404
    
    note.tags.remove(tag)

    db.session.commit()

    return jsonify({
        'message': 'Tag removed successfully',
        'note': note.to_dict()
    }), 200

@tag_bp.route('/by_tag/<int:tag_id>', methods=['GET'])
@jwt_required()
def notes_by_tag(tag_id):

    user_id = get_jwt_identity()

    tag = db.session.get(Tag,tag_id)

    if not tag:
        return jsonify({'error': 'Tag not found'}), 404
 
    if tag.user_id != int(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    
    notes = tag.notes

    return jsonify({
        'notes':[n.to_dict() for n in notes],
        'count':len(notes),
        'tag':tag.to_dict()
    }),200